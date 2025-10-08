import streamlit as st
import pandas as pd
from datetime import date

@st.cache_data(show_spinner=False)
def preview_excel(file, nrows: int = 50) -> pd.DataFrame:
    import pandas as _pd
    return _pd.read_excel(file, nrows=nrows)

def inject_styles():
    st.markdown(
        """
        <style>
        /* Основные стили */
        .stApp {
            background: linear-gradient(180deg, #0f172a 0%, #0b1220 100%);
        }
        .main .block-container {
            background: linear-gradient(180deg, #0f172a 0%, #0b1220 100%);
            padding-top: 1rem;
        }
        .metric-card { border:1px solid rgba(49,51,63,.2); border-radius:16px; padding:12px 14px; background: rgba(255,255,255,0.05); color: #e2e8f0; }
        .section-card { border:1px solid rgba(49,51,63,.2); border-radius:16px; padding:18px; background: rgba(255,255,255,0.05); color: #e2e8f0; }
        .hr-soft { height:1px; border:none; background:rgba(99,102,241,.25); margin: .75rem 0 1rem; }
        .hint { color:#94a3b8; font-style:italic; }
        
        /* Убираем светлый фон из верхней части */
        [data-testid="stHeader"] {
            background: transparent !important;
        }
        
        /* Гармонизируем заголовки с темной темой */
        .main h1, .main h2, .main h3,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #cbd5e1 !important;
        }
        
        /* Заголовки h1 - основные */
        .main h1, [data-testid="stMarkdownContainer"] h1 {
            color: #cbd5e1 !important;
        }
        
        /* Подзаголовки h2 и h3 - более мягкие */
        .main h2, [data-testid="stMarkdownContainer"] h2,
        .main h3, [data-testid="stMarkdownContainer"] h3 {
            color: #94a3b8 !important;
        }
        
        /* Общий контейнер - единый фон */
        .main, .block-container, [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }
        
        /* Стили для сайдбара */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        }
        
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        }
        
        /* Логотип/заголовок компании */
        [data-testid="stSidebar"] .sidebar-header {
            padding: 1.5rem 1rem;
            text-align: center;
            border-bottom: 2px solid rgba(99, 102, 241, 0.3);
            margin-bottom: 1.5rem;
        }
        
        [data-testid="stSidebar"] .company-logo {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        [data-testid="stSidebar"] .company-name {
            color: #e2e8f0;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: 0.05em;
        }
        
        [data-testid="stSidebar"] .company-tagline {
            color: #94a3b8;
            font-size: 0.75rem;
            margin-top: 0.25rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        
        /* Навигационные ссылки */
        [data-testid="stSidebar"] a {
            color: #cbd5e1 !important;
            text-decoration: none;
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        [data-testid="stSidebar"] a:hover {
            background: rgba(99, 102, 241, 0.2);
            color: #e0e7ff !important;
            transform: translateX(4px);
        }
        
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
            background: rgba(30, 41, 59, 0.5);
            margin: 0.25rem 0.5rem;
        }
        
        [data-testid="stSidebar"] [aria-selected="true"] {
            background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%) !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        }
        
        /* Разделитель навигации */
        [data-testid="stSidebar"] .nav-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.5), transparent);
            margin: 1rem 0;
        }
        
        /* Футер сайдбара */
        [data-testid="stSidebar"] .sidebar-footer {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem;
            background: rgba(15, 23, 42, 0.8);
            border-top: 1px solid rgba(99, 102, 241, 0.2);
            text-align: center;
            color: #64748b;
            font-size: 0.75rem;
        }
        
        /* Иконки в навигации */
        [data-testid="stSidebar"] svg {
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def sidebar_content():
    """Добавляет кастомный контент в сайдбар"""
    with st.sidebar:
        st.markdown(
            """
            <div class='sidebar-header'>
                <div class='company-logo'>🚛</div>
                <h1 class='company-name'>BH Trans</h1>
                <p class='company-tagline'>Fleet Management Pro</p>
            </div>
            """,
            unsafe_allow_html=True
        )

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

