import streamlit as st
import pandas as pd
from datetime import date


if st.session_state.active_page == "Загрузка":
    st.header("📁 Загрузка месячных данных")
    st.write("Здесь бухгалтер загружает 5 Excel-файлов по категориям. Поки без записи в БД — только UI.")

    with st.container():
        st.subheader("1) Параметры периода")
        c1, c2, c3 = st.columns([1,1,2])
        with c1:
            period_month = st.date_input("Месяц отчёта", value=date.today().replace(day=1), format="YYYY-MM-DD")
        with c2:
            currency = st.selectbox("Валюта", ["USD", "EUR"], index=0)
        with c3:
            st.write("\n")
            st.markdown("<div class='hint'>Все файлы должны содержать колонку <code>tractor_no</code>.</div>", unsafe_allow_html=True)

    st.markdown("<hr class='hr-soft'>", unsafe_allow_html=True)

    with st.container():
        st.subheader("2) Файлы по категориям")
        u1, u2 = st.columns(2)
        with u1:
            fuel_file   = st.file_uploader("⛽ Fuel (.xlsx)", type=["xlsx"], key="file_fuel")
            tolls_file  = st.file_uploader("🛣️ Tolls (.xlsx)", type=["xlsx"], key="file_tolls")
            repair_file = st.file_uploader("🔧 Repair (.xlsx)", type=["xlsx"], key="file_repair")
        with u2:
            salary_file = st.file_uploader("👷 Salary (.xlsx)", type=["xlsx"], key="file_salary")
            gross_file  = st.file_uploader("💵 Gross (.xlsx) — содержит total_rev и total_miles", type=["xlsx"], key="file_gross")

        st.markdown("<div class='help'>Подсказка: имена листов и колонок можно будет сконфигурировать позже.</div>", unsafe_allow_html=True)

    st.markdown("<hr class='hr-soft'>", unsafe_allow_html=True)

    with st.container():
        st.subheader("3) Предпросмотр и валидация")
        st.write("Показаны первые 5 строк каждого файла (если загружен).")
        pv1, pv2 = st.columns(2)
        with pv1:
            if fuel_file:
                st.caption("Fuel")
                try:
                    st.dataframe(pd.read_excel(fuel_file).head())
                except Exception as e:
                    st.error(f"Не удалось прочитать файл Fuel: {e}")
            if tolls_file:
                st.caption("Tolls")
                try:
                    st.dataframe(pd.read_excel(tolls_file).head())
                except Exception as e:
                    st.error(f"Не удалось прочитать файл Tolls: {e}")
            if repair_file:
                st.caption("Repair")
                try:
                    st.dataframe(pd.read_excel(repair_file).head())
                except Exception as e:
                    st.error(f"Не удалось прочитать файл Repair: {e}")
        with pv2:
            if salary_file:
                st.caption("Salary")
                try:
                    st.dataframe(pd.read_excel(salary_file).head())
                except Exception as e:
                    st.error(f"Не удалось прочитать файл Salary: {e}")
            if gross_file:
                st.caption("Gross (rev & miles)")
                try:
                    st.dataframe(pd.read_excel(gross_file).head())
                except Exception as e:
                    st.error(f"Не удалось прочитать файл Gross: {e}")

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔎 Валидация tractor_no")
        st.write("Здесь появится таблица траков, которых нет в справочнике \"truck\" (пока заглушка).")
        st.dataframe(pd.DataFrame({
            "tractor_no": ["1740", "9999"],
            "status": ["OK", "NOT FOUND"],
            "Комментарий": ["есть в БД", "добавить в справочник"]
        }))

        st.markdown("<br>", unsafe_allow_html=True)
        st.button("💾 Залить в БД (UPsert)", help="Пока не делает запись — только UI-кнопка")
