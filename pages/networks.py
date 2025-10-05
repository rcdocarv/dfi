import streamlit as st
import pandas as pd
import asyncio
import threading
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "monitar"
COLLECTION_NAME = "syncSystems"

client = AsyncIOMotorClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

_LOOP = asyncio.new_event_loop()
_THREAD = threading.Thread(target=_LOOP.run_forever, daemon=True)
_THREAD.start()

def run_async(coro):
    return asyncio.run_coroutine_threadsafe(coro, _LOOP).result()

async def fetch_all_documents():
    docs = [d async for d in collection.find({})]
    for doc in docs:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
    return docs

def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].astype(str)
    return df

def render():
    st.title("Comparative Analysis — Agrupado por netw_name")
    with st.spinner("A carregar..."):
        docs = run_async(fetch_all_documents())
    if not docs:
        st.warning("Nenhum documento encontrado.")
        st.stop()
    df = pd.json_normalize(docs, sep=".")
    df = sanitize_dataframe(df)
    search_term = st.text_input("Procurar sistemas", value="", placeholder="Escreve qualquer termo...")
    if search_term:
        blob = df.astype(str).agg(" ".join, axis=1).str.lower()
        df = df[blob.str.contains(search_term.lower(), na=False)]
    if "netw_name" not in df.columns:
        st.error("Campo 'netw_name' não existe nos documentos.")
        st.stop()
    counts = df["netw_name"].value_counts().reset_index()
    counts.columns = ["netw_name", "count"]
    st.dataframe(counts, use_container_width=True)
    for netw, group in df.groupby("netw_name"):
        st.subheader(f"Rede: {netw} ({len(group)})")
        st.dataframe(group, use_container_width=True)
