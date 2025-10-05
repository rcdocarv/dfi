import streamlit as st
from pages.select_systems import render as select_systems
from pages.services import (
    fetch_and_preprocess_series,
    calculate_aggregated_means,
    fetch_system_full,
    run_async,
    calibrate_model
)
from datetime import time, datetime, timedelta
from functools import reduce

import pandas as pd
import plotly.graph_objs as go

def render():
    st.header("🛠️ Calibração de Sistemas")

    # 1) Seleção de sistemas
    uids = select_systems()
    if not uids:
        st.info("Seleciona pelo menos um sistema.")
        return

    # 2) Metadados
    full_docs = {}
    for uid in uids:
        if uid not in st.session_state.systems_full:
            src, sid = uid.split("_",1)
            st.session_state.systems_full[uid] = run_async(fetch_system_full(sid))
        full_docs[uid] = st.session_state.systems_full[uid]

    def fmt(uid):
        d = full_docs[uid]
        return d.get("name") or d.get("system_name") or uid

    # 3) Referência e poluente
    ref_uid   = st.selectbox("🎯 Estação de referência", uids, format_func=fmt)
    pollutant = st.selectbox(
        "🧪 Poluente a calibrar",
        sorted({s for d in full_docs.values() for s in d.get("sensors", {})})
    )
    st.success(f"Calibrando {pollutant}")

    # 4) Covariáveis (não-ref)
    covs = {
        s for uid, d in full_docs.items() if uid != ref_uid
        for s in d.get("sensors", {})
    }
    covs.discard(pollutant)
    chosen_covs = st.multiselect("🔧 Covariáveis adicionais", sorted(covs))

    # 5) Intervalo de tempo
    c1, c2 = st.columns(2)
    with c1:
        d0 = st.date_input("Data inicial")
        t0 = st.time_input("Hora inicial", value=time(0,0))
    with c2:
        d1 = st.date_input("Data final")
        t1 = st.time_input("Hora final", value=time(23,59))
    dt0 = datetime.combine(d0, t0)
    dt1 = datetime.combine(d1, t1)
    if dt0 >= dt1:
        st.error("Data inicial deve ser anterior à data final.")
        return

    # 6) Filtro de Valores + robusto
    with st.expander("⚖️ Filtro de Valores"):
        lo     = st.number_input("Valor mínimo", -1e9, 1e9, -1e9, 0.1)
        hi     = st.number_input("Valor máximo", -1e9, 1e9,  1e9, 0.1)
        method = st.selectbox("Método robusto", ["Raw","MAD","IQR"])
        if method in ("MAD","IQR"):
            win = st.number_input("Janela (ímpares)", 3, 101, 7, 2)
            k   = st.number_input("Fator k", 1.0, 10.0, 3.0, 0.1)
        else:
            win, k = None, None

    # 7) Deslocamento temporal
    with st.expander("⏳ Deslocamento"):
        ho    = st.number_input("Horas (−/+)", -23,23,0,1)
        mi    = st.number_input("Minutos (−/+)", -59,59,0,1)
        delta = timedelta(hours=ho, minutes=mi)

    # 8) Busca e preprocessa todas as séries
    series_list = []
    for uid in uids:
        # poluente
        dfp = fetch_and_preprocess_series(
            uid, pollutant, ref_uid, dt0, dt1, lo, hi, method, win, k, delta
        )
        if dfp is not None:
            series_list.append(dfp.rename(columns={pollutant: fmt(uid)}))

        # covariáveis
        if uid != ref_uid:
            for cov in chosen_covs:
                dfc = fetch_and_preprocess_series(
                    uid, cov, ref_uid, dt0, dt1, lo, hi, method, win, k, delta
                )
                if dfc is not None:
                    series_list.append(dfc.rename(columns={cov: f"{fmt(uid)}_{cov}"}))

    if not series_list:
        st.warning("Sem dados após pré‐processamento.")
        return

    # 9) Merge e agregação para alinhar frequência
    df_all = reduce(
        lambda a, b: pd.merge(a, b, on="timestamp", how="outer"),
        series_list
    ).sort_values("timestamp")

    agg = st.selectbox("🔢 Agregação", ["Raw","Horária","Diária"])
    df_disp = {
        "Raw": df_all,
        "Horária": calculate_aggregated_means(df_all, "H"),
        "Diária": calculate_aggregated_means(df_all, "D")
    }[agg]

    # 10) Exibição
    with st.expander("🔍 Dados Agregados", expanded=False):
        st.dataframe(df_disp, use_container_width=True)

    st.subheader("📈 Série do Poluente")
    fig1 = go.Figure()
    for col in df_disp.columns:
        if col == "timestamp": continue
        fig1.add_trace(go.Scatter(
            x=df_disp["timestamp"], y=df_disp[col],
            mode="lines", name=col, connectgaps=True
        ))
    st.plotly_chart(fig1, use_container_width=True)

    # 11) Calibração
    st.subheader("⚙️ Calibração por estação Não-Referência")
    model_type = st.selectbox("Modelo", ["PLS","Polinomial"])
    if model_type == "PLS":
        ncomp = st.slider("Componentes PLS", 1, len(chosen_covs)+1, 2)
    else:
        deg = st.slider("Grau do Polinômio", 1, 5, 2)

    cal_dfs = []
    ref_label = fmt(ref_uid)

    for uid in uids:
        if uid == ref_uid: 
            continue
        station = fmt(uid)

        # monta dataset ['timestamp','y', X1,...]
        cols = ["timestamp", ref_label, station]
        cols += [f"{station}_{cov}" for cov in chosen_covs]
        ds = df_disp[cols].rename(columns={ref_label: "y", station: f"{station}_{pollutant}"})
        ds = ds.dropna()
        if ds.empty:
            st.warning(f"Sem dados válidos para {station}.")
            continue

        # calibra modelo
        y_cal, r2_full, formula = calibrate_model(
            ds,
            model_type,
            n_components=ncomp if model_type=="PLS" else None,
            poly_degree=deg       if model_type=="Polinomial" else None
        )

        # exibe o R² correto e a fórmula
        st.write(f"**{station}** — R² (full): {r2_full:.3f}")
        st.text_input(f"Fórmula de calibração ({station})", value=formula, key=f"formula_{station}")

        # gera a série calibrada
        cal_dfs.append(
            pd.DataFrame({
                "timestamp": ds["timestamp"],
                f"cali_{station}": y_cal
            })
        )

    if not cal_dfs:
        st.warning("Nenhuma calibração gerada.")
        return

    # 12) Gráfico final de calibração
    df_ref = df_disp[["timestamp", ref_label]].rename(columns={ref_label: "ref_original"})
    df_cal = reduce(lambda a,b: pd.merge(a,b,on="timestamp",how="outer"), [df_ref, *cal_dfs])
    df_cal = df_cal.sort_values("timestamp")

    st.subheader("📈 Gráfico de Calibração")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df_cal["timestamp"], y=df_cal["ref_original"],
        mode="lines", name=f"ref_{ref_label}"
    ))
    for col in df_cal.columns:
        if col in ("timestamp","ref_original"): continue
        fig2.add_trace(go.Scatter(
            x=df_cal["timestamp"], y=df_cal[col],
            mode="lines", name=col
        ))
    fig2.update_layout(xaxis_title="Timestamp", yaxis_title=pollutant)
    st.plotly_chart(fig2, use_container_width=True)
