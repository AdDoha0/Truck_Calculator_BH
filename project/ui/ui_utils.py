import streamlit as st
import pandas as pd
from datetime import date

@st.cache_data(show_spinner=False)
def preview_excel(file, nrows: int = 50) -> pd.DataFrame:
    import pandas as _pd
    return _pd.read_excel(file, nrows=nrows)

def inject_styles():
    pass

def sidebar_content():
    """Добавляет кастомный контент в сайдбар"""
    with st.sidebar:
        st.markdown("# BH Trans")
        st.markdown("*Fleet Management Pro*")
        st.divider()

@st.cache_data(show_spinner=False)
def demo_months():
    import pandas as _pd
    return _pd.to_datetime(_pd.Series(["2025-07-01","2025-08-01","2025-09-01"]))

@st.cache_data(show_spinner=False)
def demo_unit_month():
    import pandas as _pd
    df = _pd.DataFrame({
        "tractor_no": ["1740","1741","1742","1743"],
        "driver_name": ["Brandon","Tyler","Askar","Miguel"],
        "total_rev": [27300,25800,29150,24000],
        "total_miles": [9500,8800,10050,8200],
        "salary": [4000,3600,4200,3300],
        "fuel": [4250,3900,4450,3700],
        "tolls": [350,290,310,280],
        "repair": [600,450,500,480],
        "total_fixed": [3405,3440,3520,3300],
    })
    df["total_variable"] = df[["salary","fuel","tolls","repair"]].sum(axis=1)
    df["gross_profit"] = df["total_rev"] - (df["total_variable"] + df["total_fixed"])
    df["rpm"] = (df["total_rev"] / df["total_miles"]).round(3)
    df["cpm"] = ((df["total_variable"] + df["total_fixed"]) / df["total_miles"]).round(3)
    return df

