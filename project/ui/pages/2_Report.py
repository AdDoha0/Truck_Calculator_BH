import streamlit as st
from ui_utils import demo_months, demo_unit_month, sidebar_content

st.set_page_config(page_title="Отчёт • BH Trans", page_icon="📊", layout="wide")
sidebar_content()

st.header("📊 Отчёт по тракам")

months = demo_months()
month = st.selectbox("Месяц", options=months, format_func=lambda d: d.strftime("%Y-%m"))

df = demo_unit_month()

k1,k2,k3,k4 = st.columns(4)
with k1:
    st.metric("Sum(Rev)", f"${df['total_rev'].sum():,.0f}")
with k2:
    st.metric("Sum(Var)", f"${df['total_variable'].sum():,.0f}")
with k3:
    st.metric("Sum(Fixed)", f"${df['total_fixed'].sum():,.0f}")
with k4:
    st.metric("Sum(GP)", f"${df['gross_profit'].sum():,.0f}")

st.divider()

st.subheader("🧾 Таблица v_unit_month")
st.dataframe(df[[
    "tractor_no","driver_name","total_rev","total_miles","salary","fuel","tolls","repair","total_variable","total_fixed","gross_profit","rpm","cpm"
]])

st.divider()

g1,g2 = st.columns(2)
with g1:
    st.subheader("📈 GP по тракам")
    st.bar_chart(df.set_index("tractor_no")["gross_profit"])
with g2:
    st.subheader("📉 RPM / CPM по тракам")
    st.line_chart(df.set_index("tractor_no")[['rpm','cpm']])

st.subheader("⏳ Динамика GP (демо)")
trend = df["gross_profit"].sum()
st.area_chart({"2025-07": trend-2000, "2025-08": trend+500, "2025-09": trend+1200})

