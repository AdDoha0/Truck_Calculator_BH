# app.py
# -------------------------------------------------------------
# Мультистраничный фронт на Streamlit под задачу учёта по тракам.
# Поки БЕЗ логики БД/ETL, только UI/верстка + заглушки.
# -------------------------------------------------------------

import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="BH Trans • Отчёты по тракам",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 🌈 Общие стили (легкий кастом)
# -----------------------------
CUSTOM_CSS = """
<style>
.block-container { padding-top: 1rem; }
.metric-card { 
  border: 1px solid rgba(49,51,63,0.2);
  border-radius: 16px; padding: 14px 16px; background: rgba(250, 250, 252, 0.75);
}
.section-card {
  border: 1px solid rgba(49,51,63,0.2);
  border-radius: 16px; padding: 18px; background: white;
}
.help { color: #6b7280; font-size: 0.9rem; }
.hint { color: #64748b; font-style: italic; }
.hr-soft { height: 1px; border: none; background: rgba(99,102,241,0.25); margin: 0.75rem 0 1rem; }
/* кнопки навигации как полноценные */
.sidebar-btn button {width:100%; text-align:left; border-radius:12px;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------
# 🔧 Состояние (плейсхолдеры)
# -----------------------------
if "active_page" not in st.session_state:
    st.session_state.active_page = "Загрузка"

PAGES = ["Загрузка", "Отчёт", "Настройки", "Справочники"]
PAGE_ICONS = {"Загрузка":"📁","Отчёт":"📊","Настройки":"⚙️","Справочники":"📚"}

# -----------------------------
# 🧭 Сайдбар навигация (кнопки вместо радио)
# -----------------------------
with st.sidebar:
    st.title("🚚 BH Trans")
    st.caption("Отчёты по тракам • фронт без логики")
    for p in PAGES:
        label = f"{PAGE_ICONS.get(p,'•')}  {p}"
        # класс .sidebar-btn даёт нам чуть более широкую кнопку и скругление
        c = st.container()
        with c:
            clicked = st.button(label, key=f"nav_{p}", use_container_width=True)
        if clicked:
            st.session_state.active_page = p
    st.divider()
    st.markdown(f"""
**В этом MVP:**
- 5 загрузчиков файлов
- Валидация tractor_no
- Карточки KPI  
- Графики GP, RPM/CPM
- Заглушки форм фикс-расходов и справочников
    """)

# =============================================================
# 🧩 Страница: ЗАГРУЗКА
# =============================================================
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

# =============================================================
# 📊 Страница: ОТЧЁТ
# =============================================================
elif st.session_state.active_page == "Отчёт":
    st.header("📊 Отчёт по тракам")
    st.write("Выбери месяц, далее — сводная таблица и графики. Пока данные демонстрационные.")

    # Демо-месяца
    months_demo = pd.to_datetime(pd.Series(["2025-07-01", "2025-08-01", "2025-09-01"]))
    month = st.selectbox("Месяц", options=months_demo, format_func=lambda d: d.strftime("%Y-%m"))

    # Демоданные отчёта
    demo = pd.DataFrame({
        "tractor_no": ["1740", "1741", "1742", "1743"],
        "driver_name": ["Brandon", "Tyler", "Askar", "Miguel"],
        "total_rev": [27300, 25800, 29150, 24000],
        "total_miles": [9500, 8800, 10050, 8200],
        "salary": [4000, 3600, 4200, 3300],
        "fuel": [4250, 3900, 4450, 3700],
        "tolls": [350, 290, 310, 280],
        "repair": [600, 450, 500, 480],
        "total_fixed": [3405, 3440, 3520, 3300],
    })
    demo["total_variable"] = demo[["salary","fuel","tolls","repair"]].sum(axis=1)
    demo["gross_profit"] = demo["total_rev"] - (demo["total_variable"] + demo["total_fixed"])
    demo["rpm"] = (demo["total_rev"] / demo["total_miles"]).round(3)
    demo["cpm"] = ((demo["total_variable"] + demo["total_fixed"]) / demo["total_miles"]).round(3)

    # KPI карточки
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Sum(Rev)", f"${demo['total_rev'].sum():,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with k2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Sum(Var)", f"${demo['total_variable'].sum():,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with k3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Sum(Fixed)", f"${demo['total_fixed'].sum():,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with k4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Sum(GP)", f"${demo['gross_profit'].sum():,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='hr-soft'>", unsafe_allow_html=True)

    with st.container():
        st.subheader("🧾 Таблица отчёта (v_unit_month)")
        st.dataframe(demo[[
            "tractor_no","driver_name","total_rev","total_miles",
            "salary","fuel","tolls","repair","total_variable","total_fixed","gross_profit","rpm","cpm"
        ]])

    st.markdown("<hr class='hr-soft'>", unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("📈 GP по тракам")
        st.bar_chart(demo.set_index("tractor_no")["gross_profit"])
    with g2:
        st.subheader("📉 RPM / CPM по тракам")
        st.line_chart(demo.set_index("tractor_no")[["rpm","cpm"]])

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("⏳ Динамика GP (демо)")
    trend = pd.DataFrame({
        "month": ["2025-07","2025-08","2025-09"],
        "gp": [demo["gross_profit"].sum()-2000, demo["gross_profit"].sum()+500, demo["gross_profit"].sum()+1200]
    }).set_index("month")
    st.area_chart(trend)

# =============================================================
# ⚙️ Страница: НАСТРОЙКИ (фиксы)
# =============================================================
elif st.session_state.active_page == "Настройки":
    st.header("⚙️ Настройки фиксированных расходов")
    st.write("Редактирование общих и индивидуальных фикс-значений. Поки UI без связки с БД.")

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

# =============================================================
# 📚 Страница: СПРАВОЧНИКИ
# =============================================================
elif st.session_state.active_page == "Справочники":
    st.header("📚 Справочники и сервисные страницы")
    st.write("Добавление/редактирование траков, просмотр загруженных периодов, лог последних операций.")

    t1, t2, t3 = st.tabs(["Траки", "Периоды", "Логи"]) 

    with t1:
        st.subheader("Справочник траков")
        st.text_input("tractor_no", placeholder="например, 1740")
        st.button("➕ Добавить трак", help="Заглушка")
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "tractor_no": ["1740","1741","1742"],
            "status": ["active","active","inactive"],
        }))

    with t2:
        st.subheader("Загруженные периоды (демо)")
        st.dataframe(pd.DataFrame({
            "period_month": ["2025-07-01","2025-08-01","2025-09-01"],
            "files": ["5/5","4/5","2/5"],
            "status": ["complete","waiting salary","waiting fuel"]
        }))

    with t3:
        st.subheader("Логи операций (демо)")
        st.code("""
2025-09-01 12:03  Uploaded fuel.xlsx (32 rows)
2025-09-01 12:05  Uploaded tolls.xlsx (16 rows)
2025-09-01 12:06  Uploaded repair.xlsx (5 rows)
2025-09-01 12:08  Uploaded salary.xlsx (31 rows)
2025-09-01 12:12  Uploaded gross.xlsx (32 rows)
2025-09-01 12:13  Upsert to monthly_revenue: 32 rows
2025-09-01 12:13  Upsert to variable_item: fuel=32, tolls=16, repair=5, salary=31
        """)
