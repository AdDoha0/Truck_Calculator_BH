import streamlit as st
from ui_utils import inject_styles

st.set_page_config(page_title="Настройки • BH Trans", page_icon="⚙️", layout="wide")
inject_styles()

st.header("⚙️ Настройки фиксированных расходов (UI-заглушки)")

c_common, c_truck = st.tabs(["Общие (fixed_costs_common)", "Индивидуальные (fixed_costs_truck)"])

with c_common:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Общие расходы для всех траков")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ifta = st.number_input("IFTA, $/мес", min_value=0.0, value=150.0, step=10.0)
    with col2:
        ins = st.number_input("Insurance (Liability), $/мес", min_value=0.0, value=600.0, step=10.0)
    with col3:
        eld = st.number_input("ELD, $/мес", min_value=0.0, value=40.0, step=1.0)
    with col4:
        tablet = st.number_input("Tablet, $/мес", min_value=0.0, value=25.0, step=1.0)
    st.button("💾 Сохранить общие фиксы", help="Сейчас не сохраняет — заглушка")
    st.markdown("</div>", unsafe_allow_html=True)

with c_truck:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Индивидуальные по траку")
    l1, l2 = st.columns([2,3])
    with l1:
        tractor = st.text_input("tractor_no", placeholder="например, 1740")
        st.caption("Будет искаться в справочнике truck → затем подтянется truck_id")
    with l2:
        colA, colB, colC, colD = st.columns(4)
        with colA:
            tp = st.number_input("Truck payment", min_value=0.0, value=1200.0, step=10.0)
        with colB:
            trp = st.number_input("Trailer payment", min_value=0.0, value=800.0, step=10.0)
        with colC:
            pdt = st.number_input("PD Ins (Truck)", min_value=0.0, value=250.0, step=10.0)
        with colD:
            pdl = st.number_input("PD Ins (Trailer)", min_value=0.0, value=190.0, step=10.0)
    st.button("💾 Сохранить по траку", help="Сейчас не сохраняет — заглушка")
    st.markdown("</div>", unsafe_allow_html=True)

