import asyncio
import threading
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import pandas as pd
import numpy as np
from datetime import timedelta
from typing import Optional, Tuple

from sklearn.cross_decomposition import PLSRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import r2_score

# --- Config Mongo ---
MONGO_URI      = "mongodb://localhost:27017"
DB_NAME        = "monitar"
SYNC_COLL_NAME = "syncSystems"

client    = AsyncIOMotorClient(MONGO_URI)
sync_coll = client[DB_NAME][SYNC_COLL_NAME]

# --- Event loop async em background ---
_LOOP   = asyncio.new_event_loop()
_THREAD = threading.Thread(target=_LOOP.run_forever, daemon=True)
_THREAD.start()

def run_async(coro):
    """Executa uma coroutine no loop criado acima e retorna o resultado."""
    return asyncio.run_coroutine_threadsafe(coro, _LOOP).result()

async def fetch_systems_light():
    proj = {"id":1, "name":1, "netw_name":1, "data_src":1, "_id":0}
    docs = [d async for d in sync_coll.find({}, proj)]
    for d in docs:
        d["id"] = str(d["id"])
    return docs

async def fetch_system_full(sys_id: str):
    try:
        doc = await sync_coll.find_one({"_id": ObjectId(sys_id)})
    except:
        doc = None
    if not doc:
        doc = await sync_coll.find_one({"id": sys_id})
    if doc:
        doc["id"] = str(doc["id"])
    return doc

async def fetch_sensor_data_mongo(
    data_src: str,
    system_id: str,
    sensor: str,
    start_dt: str,
    end_dt: str
) -> pd.DataFrame:
    collection_name = f"{data_src}_{system_id}"
    collection = client[DB_NAME][collection_name]
    query = {"dt": {"$gte": start_dt, "$lte": end_dt}}
    projection = {"_id": 0, "dt": 1, sensor: 1}

    docs = [d async for d in collection.find(query, projection)]
    return pd.DataFrame(docs) if docs else pd.DataFrame()

def calculate_aggregated_means(df: pd.DataFrame, freq: str) -> pd.DataFrame:
    """
    Resample por frequência ('H' ou 'D') e retorna a média.
    Assume df com coluna 'timestamp'.
    """
    tmp = df.set_index("timestamp")
    agg = tmp.resample(freq).mean()
    return agg.reset_index()

def robust_filter(
    df: pd.DataFrame,
    col: str,
    method: str,
    window: int,
    k: float
) -> pd.DataFrame:
    """
    Filtra outliers de df[col] usando MAD ou IQR em janela rolante.
    Se method == "Raw", devolve df inalterado.
    """
    if method == "MAD":
        med = df[col].rolling(window, center=True).median()
        mad = df[col].rolling(window, center=True).apply(
            lambda x: np.median(np.abs(x - np.median(x))), raw=True
        )
        return df[(df[col] - med).abs() <= k * mad]

    if method == "IQR":
        q1 = df[col].rolling(window, center=True).quantile(0.25)
        q3 = df[col].rolling(window, center=True).quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - k * iqr, q3 + k * iqr
        return df[df[col].between(lower, upper)]

    return df

def fetch_and_preprocess_series(
    uid: str,
    sensor: str,
    ref_uid: str,
    dt0: pd.Timestamp,
    dt1: pd.Timestamp,
    lo: float,
    hi: float,
    method: str,
    window: int,
    k: float,
    delta: timedelta
) -> Optional[pd.DataFrame]:
    """
    Busca e prepara a série do `sensor` para estação `uid`:
      - renomeia dt→timestamp e sensor→coluna
      - filtra [lo, hi]
      - aplica robust_filter se uid != ref_uid
      - aplica deslocamento delta se uid != ref_uid
    Retorna df[['timestamp', sensor]] ou None.
    """
    src, sid = uid.split("_", 1)
    raw = run_async(fetch_sensor_data_mongo(
        src, sid, sensor,
        f"isoDate({dt0.isoformat()[:-3]})",
        f"isoDate({dt1.isoformat()[:-3]})"
    ))
    if raw is None or raw.empty:
        return None

    df = raw.rename(columns={"dt": "timestamp", sensor: sensor})
    df["timestamp"] = pd.to_datetime(
        df["timestamp"].str.replace(r"^isoDate\((.*)\)$", r"\1", regex=True)
    )
    df = df[(df[sensor] >= lo) & (df[sensor] <= hi)]

    if uid != ref_uid and method in ("MAD", "IQR"):
        df = robust_filter(df, sensor, method, window, k)

    if uid != ref_uid:
        df["timestamp"] += delta

    return df[["timestamp", sensor]]

def calibrate_model(
    ds: pd.DataFrame,model_type: str,n_components: int = 2,poly_degree: int = 2) -> Tuple[np.ndarray, float, str]:
    """
    ds: DataFrame com colunas ['timestamp','y', X1, X2, ...]
    model_type: 'PLS' | 'Polinomial' | 'MLR' | 'MLRS'
    n_components: para PLS
    poly_degree: para Polinomial
    Retorna:
      - y_cal (np.ndarray)
      - r2_full (float)
      - formula (str)
    """
    # prepara X e y
    X = ds.drop(columns=["timestamp", "y"])
    y = ds["y"].values

    # instancia modelo
    if model_type == "PLS":
        model = PLSRegression(n_components=n_components)

    elif model_type == "Polinomial":
        model = Pipeline([
            ("poly", PolynomialFeatures(degree=poly_degree, include_bias=False)),
            ("scaler", StandardScaler()),
            ("lr", LinearRegression())
        ])

    elif model_type == "MLR":
        model = LinearRegression()

    elif model_type == "MLRS":
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("lr", LinearRegression())
        ])

    else:
        raise ValueError(f"Modelo desconhecido: {model_type}")

    # ajusta no dataset completo
    model.fit(X, y)
    y_cal = model.predict(X)

    # R² no dataset inteiro (igual ao que você computa no Excel)
    r2_full = float(r2_score(y, y_cal))

    # coeficientes e intercept
    if model_type == "PLS":
        coefs = pd.Series(model.coef_.ravel(), index=X.columns)
        intercept = y.mean() - (coefs.values * X.mean()).sum()

    elif model_type == "Polinomial":
        lr = model.named_steps["lr"]
        feats = model.named_steps["poly"].get_feature_names_out(X.columns)
        coefs = pd.Series(lr.coef_, index=feats)
        intercept = float(lr.intercept_)

    elif model_type == "MLR":
        coefs = pd.Series(model.coef_, index=X.columns)
        intercept = float(model.intercept_)

    else:  # MLRS
        lr = model.named_steps["lr"]
        coefs = pd.Series(lr.coef_, index=X.columns)
        intercept = float(lr.intercept_)

    terms = " + ".join(f"{coef:.3f}*{name}" for name, coef in coefs.items())
    formula = f"y = {intercept:.3f} + {terms}"

    return y_cal, r2_full, formula