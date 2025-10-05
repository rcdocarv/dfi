# pages/select_systems.py

import streamlit as st
import pandas as pd

from pages.services import run_async, fetch_systems_light, fetch_system_full
from pages.utils    import sanitize_dataframe

def render() -> list[str]:
    st.header("🔎 Seleção de Sistemas")

    # Inicializa estados
    st.session_state.setdefault("systems_light", None)
    st.session_state.setdefault("systems_full", {})
    st.session_state.setdefault("selected_systems", [])
    st.session_state.setdefault("selected_labels", [])

    # 1) Carrega sistemas leves
    if st.session_state.systems_light is None:
        with st.spinner("Carregando lista de sistemas..."):
            st.session_state.systems_light = run_async(fetch_systems_light())

    docs = st.session_state.systems_light or []
    if not docs:
        st.warning("Nenhum sistema encontrado.")
        return []

    # 2) DataFrame e filtros
    df = pd.DataFrame(docs)
    df = sanitize_dataframe(df)

    netw_names = sorted(df["netw_name"].fillna("Sem rede").unique().tolist())
    netw_names.insert(0, "Todos")

    col1, col2, col3 = st.columns([1.2, 1.5, 3])
    with col1:
        sel_netw_name = st.selectbox("🌐 Network", netw_names, index=0)
    with col2:
        search_term = st.text_input("🔍 Busca livre", placeholder="Nome, ID ou netw_name...")

    dff = df.copy()
    if sel_netw_name != "Todos":
        dff = dff[dff["netw_name"] == sel_netw_name]
    if search_term:
        mask = (
            dff.astype(str)
               .agg(" ".join, axis=1)
               .str.lower()
               .str.contains(search_term.lower(), na=False)
        )
        dff = dff[mask]

    # 3) Identificador único e rótulos
    dff["uid"] = dff.apply(lambda x: f"{x['data_src']}_{x['id']}", axis=1)
    dff["label"] = dff.apply(
        lambda x: f"{x.get('name') or x.get('system_name') or '(Sem nome)'} — {x['uid']}",
        axis=1
    )
    label_to_uid = dict(zip(dff["label"], dff["uid"]))
    uid_to_row   = {x["uid"]: x for _, x in dff.iterrows()}
    options      = dff["label"].tolist()

    # 4) Botões de ação — atualizam antes do widget ser criado
    col_btn, _ = st.columns([1, 5])
    with col_btn:
        b1, b2 = st.columns(2)
        with b1:
            if st.button("✅ Todos"):
                st.session_state.selected_labels = options
                st.session_state.selected_systems = [label_to_uid[lbl] for lbl in options]
                st.rerun()
        with b2:
            st.button(
                "❌ Limpar",
                disabled=not st.session_state.selected_labels,
                on_click=lambda: (
                    st.session_state.update({
                        "selected_labels": [],
                        "selected_systems": []
                    }),
                    st.rerun()
                )
            )

    # 5) Multiselect principal — usa apenas o valor já definido
    with col3:
        selected_labels = st.multiselect(
            "📋 Sistemas disponíveis",
            options=options,
            default=st.session_state.selected_labels,
            key="selected_labels"
        )

    # 6) Atualiza lista de UIDs e busca dados completos
    selected_uids = [label_to_uid[lbl] for lbl in selected_labels]
    st.session_state.selected_systems = selected_uids

    for uid in selected_uids:
        if uid not in st.session_state.systems_full:
            data_src, sys_id = uid.split("_", 1)
            full = run_async(fetch_system_full(sys_id))  # adapta se necessário
            if full:
                st.session_state.systems_full[uid] = full

    # 7) Tabela dos selecionados
    if selected_uids:
        st.subheader("📊 Sistemas Selecionados")

        def format_uid(uid):
            doc = st.session_state.systems_full.get(uid, {})
            name = doc.get("name") or doc.get("system_name") or uid
            return f"{name} — {uid}"

        for uid in selected_uids:
            doc = st.session_state.systems_full.get(uid, {})
            with st.expander(format_uid(uid), expanded=False):
                st.write({
                    "ID": uid,
                    "Nome": doc.get("name") or doc.get("system_name"),
                    "Origem": doc.get("data_src"),
                    "Network": doc.get("netw_name"),
                    "Localização": doc.get("location", "—"),
                    "Outros campos": {
                        k: v for k, v in doc.items()
                        if k not in ["id", "name", "system_name", "data_src", "netw_name", "location"]
                    }
            })

    return selected_uids
