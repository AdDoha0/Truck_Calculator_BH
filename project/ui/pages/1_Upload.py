import streamlit as st
import pandas as pd
from datetime import date
from ui_utils import preview_excel, sidebar_content

st.set_page_config(page_title="Загрузка • BH Trans", page_icon="📁", layout="wide")
sidebar_content()

st.header("📁 Загрузка месячных данных")

with st.container():
    st.subheader("1) Параметры периода")
    c1, c2, c3 = st.columns([1,1,2])
    with c1:
        period_month = st.date_input("Месяц отчёта", value=date.today().replace(day=1), format="YYYY-MM-DD")
    with c2:
        currency = st.selectbox("Валюта", ["USD","EUR"], index=0)
    with c3:
        st.info("💡 Все Excel должны содержать колонку `tractor_no`.")

st.divider()

with st.container():
    st.subheader("2) Файлы по категориям")
    u1, u2 = st.columns(2)
    with u1:
        fuel_file   = st.file_uploader("⛽ Fuel (.xlsx)", type=["xlsx"], key="fuel")
        tolls_file  = st.file_uploader("🛣️ Tolls (.xlsx)", type=["xlsx"], key="tolls")
        repair_file = st.file_uploader("🔧 Repair (.xlsx)", type=["xlsx"], key="repair")
    with u2:
        salary_file = st.file_uploader("👷 Salary (.xlsx)", type=["xlsx"], key="salary")
        gross_file  = st.file_uploader("💵 Gross (.xlsx) — total_rev и total_miles", type=["xlsx"], key="gross")

st.divider()

with st.container():
    st.subheader("3) Предпросмотр и валидация")
    pv1, pv2 = st.columns(2)
    with pv1:
        if fuel_file:
            st.caption("Fuel")
            st.dataframe(preview_excel(fuel_file).head())
        if tolls_file:
            st.caption("Tolls")
            st.dataframe(preview_excel(tolls_file).head())
        if repair_file:
            st.caption("Repair")
            st.dataframe(preview_excel(repair_file).head())
    with pv2:
        if salary_file:
            st.caption("Salary")
            st.dataframe(preview_excel(salary_file).head())
        if gross_file:
            st.caption("Gross (rev & miles)")
            st.dataframe(preview_excel(gross_file).head())

    st.subheader("🔎 Валидация tractor_no (демо)")
    st.dataframe(pd.DataFrame({"tractor_no":["1740","9999"], "status":["OK","NOT FOUND"], "Комментарий":["есть в БД","добавить в справочник"]}))


st.button("💾 Залить в БД (UPsert)", help="Пока без логики — заглушка")

