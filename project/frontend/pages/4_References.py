import streamlit as st
import pandas as pd
from ui_utils import inject_styles

st.set_page_config(page_title="Справочники • BH Trans", page_icon="📚", layout="wide")
inject_styles()

st.header("📚 Справочники и сервисные страницы")

T1, T2, T3 = st.tabs(["Траки", "Периоды", "Логи"]) 

with T1:
    st.subheader("Справочник траков")
    st.text_input("tractor_no", placeholder="например, 1740")
    st.button("➕ Добавить трак", help="Заглушка")
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "tractor_no": ["1740","1741","1742"],
        "status": ["active","active","inactive"],
    }))

with T2:
    st.subheader("Загруженные периоды (демо)")
    st.dataframe(pd.DataFrame({
        "period_month": ["2025-07-01","2025-08-01","2025-09-01"],
        "files": ["5/5","4/5","2/5"],
        "status": ["complete","waiting salary","waiting fuel"]
    }))

with T3:
    st.subheader("Логи операций (демо)")
    st.code(
        """
2025-09-01 12:03  Uploaded fuel.xlsx (32 rows)
2025-09-01 12:05  Uploaded tolls.xlsx (16 rows)
2025-09-01 12:06  Uploaded repair.xlsx (5 rows)
2025-09-01 12:08  Uploaded salary.xlsx (31 rows)
2025-09-01 12:12  Uploaded gross.xlsx (32 rows)
2025-09-01 12:13  Upsert to monthly_revenue: 32 rows
2025-09-01 12:13  Upsert to variable_item: fuel=32, tolls=16, repair=5, salary=31
        """
    )

