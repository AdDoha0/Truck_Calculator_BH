import streamlit as st
from ui_utils import inject_styles

st.set_page_config(
    page_title="BH Trans • Отчёты по тракам",
    page_icon="🚛",
    layout="wide",
)

inject_styles()

st.title("🚛 BH Trans — дашборд по тракам")

st.markdown(
    """
    Добро пожаловать! Это многостраничное приложение на Streamlit, 
    оформленное через **официальную структуру `pages/`**.

    Используйте меню слева, чтобы перейти на страницы:
    - **Upload** — пять файлов (fuel, tolls, repair, salary, gross)
    - **Report** — таблица v_unit_month, KPI и графики
    - **Settings** — фиксы общие + по траку
    - **References** — траки, периоды, логи

    ✨ Сейчас это только фронт (без БД и логики). Все элементы кликабельны, но данные — демо.
    """
)

st.info("Подсказка: это домашняя страница. Навигация и URL — официальные от Streamlit (директория pages/).")

