import streamlit as st
import pandas as pd
import numpy as np
import asyncio
import threading
from datetime import date, time, datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import plotly.express as px
import plotly.graph_objects as go

# --- Config Mongo ---
MONGO_URI      = "mongodb://localhost:27017"
DB_NAME        = "monitar"
SYNC_COLL_NAME = "syncSystems"

client    = AsyncIOMotorClient(MONGO_URI)
sync_coll = client[DB_NAME][SYNC_COLL_NAME]

# --- Event loop async ---
_LOOP   = asyncio.new_event_loop()
_THREAD = threading.Thread(target=_LOOP.run_forever, daemon=True)
_THREAD.start()

def run_async(coro):
    return asyncio.run_coroutine_threadsafe(coro, _LOOP).result()

# --- Busca leve dos sistemas ---
async def fetch_systems_light():
    proj = {"id":1, "name":1, "system_name":1, "netw_name":1, "data_src":1}
    docs = [d async for d in sync_coll.find({}, proj)]
    for d in docs:
        d["id"] = str(d["id"])
    return docs

# --- Busca completa de um sistema ---
async def fetch_system_full(sys_id: str):
    try: doc = await sync_coll.find_one({"_id": ObjectId(sys_id)})
    except: doc = None
    if not doc: doc = await sync_coll.find_one({"id": sys_id})
    if doc: doc["id"] = str(doc["id"])
    return doc

# --- Busca de dados brutos ---
async def fetch_data_for_system(data_src, system_id, pollutant, start_dt, end_dt):
    coll_name = f"{data_src}_{system_id}"
    coll = client[DB_NAME][coll_name]
    start_str = f"isoDate({start_dt:%Y-%m-%dT%H:%M})"
    end_str   = f"isoDate({end_dt:%Y-%m-%dT%H:%M})"
    cursor = coll.find(
        {"dt": {"$gte": start_str, "$lte": end_str}},
        {"dt":1, pollutant:1, "_id":0}
    ).sort("dt", 1)
    return [d async for d in cursor]

def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for c in df.columns:
        if df[c].dtype == "O":
            df[c] = df[c].astype(str)
    return df

def render():
    st.title("Comparative — Seleção por Network")

    # 0) Inicialização do session_state
    defaults = {
        "systems_light":      None,
        "systems_full":       {},
        "selected_systems":   [],
        "selected_sensors":   []
    }
    for key, default in defaults.items():
        st.session_state.setdefault(key, default)

    # 1) Carrega lista leve de sistemas
    if st.session_state.systems_light is None:
        with st.spinner("A carregar sistemas..."):
            st.session_state.systems_light = run_async(fetch_systems_light())

    docs_light = st.session_state.systems_light or []
    if not docs_light:
        st.warning("Nenhum sistema encontrado.")
        return

    # 2) Monta DataFrame de sistemas leves
    df = pd.DataFrame(docs_light)
    df = sanitize_dataframe(df)
    if "netw_name" in df.columns and "network" not in df.columns:
        df.rename(columns={"netw_name": "network"}, inplace=True)

    # 3) Filtros de data/hora
    st.markdown("#### Filtros")
    c1, c2, c3, c4 = st.columns([3, 1, 3, 1])
    with c1:
        start_date = st.date_input("Data inicial", date.today(), format="DD/MM/YYYY")
    with c2:
        start_time = st.time_input("Hora inicial", time(0, 0))
    with c3:
        end_date   = st.date_input("Data final", date.today(), format="DD/MM/YYYY")
    with c4:
        end_time   = st.time_input("Hora final", time(23, 59))

    start_dt = datetime.combine(start_date, start_time)
    end_dt   = datetime.combine(end_date,   end_time)
    if start_dt > end_dt:
        st.error("Data/hora final não pode ser anterior à inicial.")
        return
    st.success(f"Período: {start_dt:%d/%m/%Y %H:%M} → {end_dt:%d/%m/%Y %H:%M}")

    # 4) Campo de busca geral
    st.markdown("#### Pesquisa")
    termo = st.text_input("Pesquisar estações", placeholder="Filtro geral...", label_visibility="collapsed")
    if termo:
        mask = (
            df.astype(str)
              .agg(" ".join, axis=1)
              .str.lower()
              .str.contains(termo.lower(), na=False)
        )
        df = df[mask]

    # 5) Listagem de estações por network
    st.markdown("#### Estações por Network")
    for netw, grp in df.groupby("network"):
        with st.expander(f"{netw} ({len(grp)})"):
            for _, row in grp.iterrows():
                sid      = row["id"]
                name     = row.get("name") or row.get("system_name") or "(Sem nome)"
                data_src = row.get("data_src", "?")
                key      = f"chk_{netw}_{sid}"
                checked  = sid in st.session_state.selected_systems

                if st.checkbox("", key=key, value=checked):
                    if sid not in st.session_state.selected_systems:
                        st.session_state.selected_systems.append(sid)
                        full = run_async(fetch_system_full(sid))
                        if full:
                            st.session_state.systems_full[sid] = full
                else:
                    if sid in st.session_state.selected_systems:
                        st.session_state.selected_systems.remove(sid)
                        st.session_state.systems_full.pop(sid, None)

                st.markdown(f"**{name}** ({data_src}) — {sid}")

    # 6) Seleção de sensores disponíveis
    sensors = []
    for doc in st.session_state.systems_full.values():
        sensors += [
            str(k).strip() for k in (doc.get("sensors") or {}).keys()
            if str(k).strip()
        ]
    sensors = sorted(set(sensors))
    sel_sensors = st.multiselect(
        "Escolha sensores",
        options=sensors,
        default=[],
        placeholder="Sem sensores...",
        label_visibility="collapsed"
    )
    st.session_state.selected_sensors = sel_sensors

    # 7) Resample
    resample_opt = st.selectbox("Resample", ["Original", "Horária", "Diária"], index=1)
    rule_map     = {"Horária": "1H", "Diária": "24H"}

    sel_sys     = st.session_state.selected_systems
    sel_sensors = st.session_state.selected_sensors
    if not (sel_sys and sel_sensors):
        return

    # 7.1) Filtros de valor global
    st.markdown("---")
    st.markdown("#### Filtrar valores extremos")
    bound = 1e9
    min_val = st.number_input(
        "Valor mínimo (abaixo será anulado)",
        min_value=-bound,
        max_value=bound,
        value=-bound,
        step=0.1,
        format="%.2f"
    )
    max_val = st.number_input(
        "Valor máximo (acima será anulado)",
        min_value=-bound,
        max_value=bound,
        value=bound,
        step=0.1,
        format="%.2f"
    )

    # 8) Escolha de referência e offset
    st.markdown("### Ajuste de tempo para correlação")
    ref = st.selectbox(
        "Sistema referência",
        options=sel_sys,
        format_func=lambda i: f"{st.session_state.systems_full[i]['name']} — {i}"
    )
    step   = st.number_input("Passo do slider (minutos)", min_value=1, max_value=60, value=1)
    offset = st.slider("Deslocar não-ref (minutos)", -180, 180, 0, step=step)
    ref_label = f"{st.session_state.systems_full[ref]['name']} — {ref}"

    # 9) Loop por cada poluente
    for pollutant in sel_sensors:
        raws, labels = [], []

        # 9.1) Busca de dados e aplicação de filtros
        for sid in sel_sys:
            full = st.session_state.systems_full[sid]
            raw = run_async(fetch_data_for_system(
                full["data_src"], sid, pollutant, start_dt, end_dt
            ))
            if not raw:
                continue

            df_r = pd.DataFrame(raw)
            df_r["dt"] = pd.to_datetime(
                df_r["dt"].str.extract(r"isoDate\((.+)\)")[0],
                format="%Y-%m-%dT%H:%M"
            )
            lbl = f"{full['name']} — {sid}"
            df_r = df_r.set_index("dt")[[pollutant]].rename(columns={pollutant: lbl})
            df_r[lbl] = df_r[lbl].where(df_r[lbl] >= min_val, np.nan)
            df_r[lbl] = df_r[lbl].where(df_r[lbl] <= max_val, np.nan)

            raws.append(df_r)
            labels.append(lbl)

        if not raws:
            st.warning(f"Sem dados para {pollutant}")
            continue

        # 9.2) Offset + resample
        shifted = []
        for df_r, lbl in zip(raws, labels):
            df_tmp = df_r.copy()
            if lbl != ref_label and offset:
                df_tmp.index = df_tmp.index + pd.Timedelta(minutes=offset)
            df_rs = df_tmp.resample(rule_map.get(resample_opt, "1H")).mean() \
                    if resample_opt != "Original" else df_tmp
            shifted.append(df_rs)

        # 9.3) Merge e toggle de exibição da tabela
        df_merged = pd.concat(shifted, axis=1, join="outer")
        df_table  = df_merged.reset_index().rename(columns={df_merged.index.name or "dt": "datetime"})

        show_tbl = st.checkbox(
            f"Mostrar tabela de {pollutant}",
            value=True,
            key=f"show_tbl_{pollutant}"
        )
        if show_tbl:
            st.subheader(f"{pollutant} — Tabela (offset {offset} min)")
            st.dataframe(df_table)

        # 9.4) Gráfico de séries
        st.subheader(f"{pollutant} — Gráfico (offset {offset} min)")
        df_long = df_table.melt(
            id_vars="datetime",
            value_vars=labels,
            var_name="Sistema",
            value_name=pollutant
        )
        fig = px.line(df_long, x="datetime", y=pollutant, color="Sistema", markers=True)
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        # 9.5) Correlação e série calibrada “cali_…”
        st.markdown(f"**Correlação de Pearson para {pollutant}:**")
        df_corr = df_merged.dropna()
        if df_corr.empty:
            st.warning("Sem sobreposição de dados após o offset.")
            continue

        x_ref     = df_corr[ref_label]
        mu_xref   = x_ref.mean()
        sigma_xref = x_ref.std()

        for lbl in labels:
            if lbl == ref_label:
                continue

            y        = df_corr[lbl]
            mu_y     = y.mean()
            sigma_y  = y.std()
            r        = x_ref.corr(y)
            # invertendo regressão para predizer x_ref a partir de y
            m_inv    = r * (sigma_xref / sigma_y)
            b_inv    = mu_xref - m_inv * mu_y
            cali     = m_inv * y + b_inv
            cali_lbl = f"cali_{lbl}"

            r2 = r**2
            st.markdown(f"- **{lbl}** vs **{ref_label}**: R² = {r2:.4f} (r = {r:.3f})")

            # scatter/regressão
            fig_reg = go.Figure()
            fig_reg.add_trace(go.Scatter(x=y,     y=x_ref, mode="markers", name=lbl))
            fig_reg.add_trace(go.Scatter(x=y,     y=cali,  mode="lines",  name=cali_lbl))
            st.plotly_chart(fig_reg, use_container_width=True)

            # gráfico temporal
            st.subheader(f"Série temporal: {ref_label} vs {cali_lbl}")
            df_time = pd.DataFrame({
                "datetime":  df_corr.index,
                ref_label:   x_ref.values,
                cali_lbl:    cali.values
            })
            fig_time = px.line(
                df_time,
                x="datetime",
                y=[ref_label, cali_lbl],
                labels={"value": pollutant, "variable": "Série"}
            )
            fig_time.update_layout(title=f"{ref_label} vs {cali_lbl}", hovermode="x unified")
            st.plotly_chart(fig_time, use_container_width=True)

if __name__=="__main__":
    render()
