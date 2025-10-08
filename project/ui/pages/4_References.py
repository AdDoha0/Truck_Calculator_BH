import streamlit as st
import pandas as pd
from ui_utils import inject_styles, sidebar_content
from db_utils import (
    init_database,
    create_truck,
    get_all_trucks, 
    get_truck_by_id,
    update_truck,
    delete_truck,
    get_truck_costs,
    update_truck_costs,
    get_common_costs,
    update_common_costs
)

st.set_page_config(page_title="Справочники • BH Trans", page_icon="📚", layout="wide")
inject_styles()
sidebar_content()

# Инициализация БД
init_database()

st.header("📚 Справочники и сервисные страницы")

T1, T2, T3, T4 = st.tabs(["🚛 Траки", "💰 Фиксированные расходы", "📅 Периоды", "📋 Логи"]) 

with T1:
    st.subheader("Управление траками")
    
    # ========== ДОБАВЛЕНИЕ НОВОГО ТРАКА ==========
    st.markdown("### ➕ Добавить новый трак")
    
    with st.form("add_truck_form"):
        new_tractor_no = st.text_input(
            "Номер трака",
            placeholder="например: 1740, ABC123, TR001",
            help="Уникальный идентификатор трака"
        )
        submit_add = st.form_submit_button("➕ Добавить трак", type="primary")
        
        if submit_add:
            if new_tractor_no:
                create_truck(new_tractor_no)
                st.rerun()
            else:
                st.error("Введите номер трака!")
    
    st.divider()
    
    # ========== СПИСОК ТРАКОВ ==========
    st.markdown("### 📋 Список траков")
    
    trucks = get_all_trucks()
    
    if not trucks:
        st.info("📭 Траки не найдены. Добавьте первый трак выше.")
    else:
        # Создаем DataFrame для отображения
        df = pd.DataFrame(trucks)
        df = df.rename(columns={
            "id": "ID",
            "tractor_no": "Номер трака",
            "monthly_rows_count": "Месячных записей",
            "fixed_costs_count": "Фикс. расходов"
        })
        
        # Отображение таблицы с возможностью выбора
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Номер трака": st.column_config.TextColumn("Номер трака", width="medium"),
                "Месячных записей": st.column_config.NumberColumn("Месячных записей", width="small"),
                "Фикс. расходов": st.column_config.NumberColumn("Фикс. расходов", width="small")
            }
        )
        
        st.markdown(f"**Всего траков:** {len(trucks)}")
        
        # ========== РЕДАКТИРОВАНИЕ/УДАЛЕНИЕ ==========
        st.markdown("### ✏️ Редактировать/Удалить трак")
        
        truck_options = {f"{truck['tractor_no']} (ID: {truck['id']})": truck['id'] 
                        for truck in trucks}
        
        selected_truck_label = st.selectbox(
            "Выберите трак для редактирования",
            options=list(truck_options.keys()),
            help="Выберите трак из списка"
        )
        
        if selected_truck_label:
            selected_truck_id = truck_options[selected_truck_label]
            truck_data = get_truck_by_id(selected_truck_id)
            
            if truck_data:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Форма редактирования
                    with st.form(f"edit_truck_form_{selected_truck_id}"):
                        st.write(f"**Редактирование трака ID: {truck_data['id']}**")
                        
                        new_tractor_no = st.text_input(
                            "Новый номер трака",
                            value=truck_data['tractor_no'],
                            help="Измените номер трака"
                        )
                        
                        submit_edit = st.form_submit_button("💾 Сохранить изменения", type="primary")
                        
                        if submit_edit:
                            if new_tractor_no:
                                if update_truck(selected_truck_id, new_tractor_no):
                                    st.rerun()
                            else:
                                st.error("Номер трака не может быть пустым!")
                
                with col2:
                    # Информация и удаление
                    st.markdown("**Информация:**")
                    st.write(f"• Месячных записей: {truck_data['monthly_rows_count']}")
                    st.write(f"• Фиксированных расходов: {truck_data['fixed_costs_count']}")
                    
                    # Кнопка удаления
                    if truck_data['monthly_rows_count'] > 0:
                        st.warning("⚠️ Нельзя удалить трак с месячными записями")
                    else:
                        if st.button("🗑️ Удалить трак", 
                                   key=f"delete_{selected_truck_id}",
                                   help="Безвозвратное удаление трака"):
                            if delete_truck(selected_truck_id):
                                st.rerun()

with T2:
    st.subheader("💰 Управление фиксированными расходами")
    
    # Общие фиксированные расходы
    st.markdown("### 🌍 Общие фиксированные расходы (применяются ко всем тракам)")
    
    common_costs = get_common_costs()
    
    with st.form("common_costs_form"):
        st.markdown("**Редактировать общие расходы:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ifta = st.number_input("IFTA ($)", value=common_costs['ifta'], min_value=0.0, step=10.0)
            insurance = st.number_input("Страхование бизнеса ($)", value=common_costs['insurance'], min_value=0.0, step=10.0)
            eld = st.number_input("ELD устройство ($)", value=common_costs['eld'], min_value=0.0, step=1.0)
        
        with col2:
            tablet = st.number_input("Планшет/навигация ($)", value=common_costs['tablet'], min_value=0.0, step=1.0)
            tolls = st.number_input("Базовые дорожные сборы ($)", value=common_costs['tolls'], min_value=0.0, step=10.0)
        
        # Показать общую сумму
        total_common = ifta + insurance + eld + tablet + tolls
        st.markdown(f"**Общая сумма общих расходов: ${total_common:,.2f}/месяц**")
        
        submit_common = st.form_submit_button("💾 Сохранить общие расходы", type="primary")
        
        if submit_common:
            success = update_common_costs(
                ifta=ifta,
                insurance=insurance,
                eld=eld,
                tablet=tablet,
                tolls=tolls
            )
            if success:
                st.rerun()
    
    st.divider()
    
    # Расходы по тракам
    st.markdown("### 🚛 Фиксированные расходы по тракам")
    
    trucks = get_all_trucks()
    
    if not trucks:
        st.info("📭 Сначала создайте траки во вкладке 'Траки'")
    else:
        truck_options = {f"{truck['tractor_no']} (ID: {truck['id']})": truck['id'] 
                        for truck in trucks}
        
        selected_truck_label = st.selectbox(
            "Выберите трак для настройки расходов",
            options=list(truck_options.keys()),
            help="Выберите трак для редактирования его фиксированных расходов"
        )
        
        if selected_truck_label:
            selected_truck_id = truck_options[selected_truck_label]
            truck_costs = get_truck_costs(selected_truck_id)
            
            with st.form(f"truck_costs_form_{selected_truck_id}"):
                st.markdown(f"**Расходы трака: {selected_truck_label}**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    truck_payment = st.number_input(
                        "Выплата за трак ($)", 
                        value=truck_costs['truck_payment'], 
                        min_value=0.0, 
                        step=50.0,
                        help="Месячная выплата за трак (лизинг/кредит)"
                    )
                    trailer_payment = st.number_input(
                        "Выплата за прицеп ($)", 
                        value=truck_costs['trailer_payment'], 
                        min_value=0.0, 
                        step=50.0,
                        help="Месячная выплата за прицеп"
                    )
                
                with col2:
                    truck_insurance = st.number_input(
                        "Страхование трака ($)", 
                        value=truck_costs['physical_damage_insurance_truck'],
                        min_value=0.0, 
                        step=10.0,
                        help="Физическое страхование трака"
                    )
                    trailer_insurance = st.number_input(
                        "Страхование прицепа ($)", 
                        value=truck_costs['physical_damage_insurance_trailer'],
                        min_value=0.0, 
                        step=10.0,
                        help="Физическое страхование прицепа"
                    )
                
                # Показать общую сумму для этого трака
                total_truck = truck_payment + trailer_payment + truck_insurance + trailer_insurance
                total_with_common = total_truck + total_common
                
                st.markdown(f"**Итого для трака: ${total_truck:,.2f}/месяц**")
                st.markdown(f"**Общий фикс (с общими расходами): ${total_with_common:,.2f}/месяц**")
                
                submit_truck = st.form_submit_button("💾 Сохранить расходы трака", type="primary")
                
                if submit_truck:
                    success = update_truck_costs(
                        selected_truck_id,
                        truck_payment=truck_payment,
                        trailer_payment=trailer_payment,
                        physical_damage_insurance_truck=truck_insurance,
                        physical_damage_insurance_trailer=trailer_insurance
                    )
                    if success:
                        st.rerun()

with T3:
    st.subheader("Загруженные периоды (демо)")
    st.info("🚧 Эта функция будет реализована при добавлении логики загрузки файлов")
    st.dataframe(pd.DataFrame({
        "period_month": ["2025-07-01","2025-08-01","2025-09-01"],
        "files": ["5/5","4/5","2/5"],
        "status": ["complete","waiting salary","waiting fuel"]
    }))

with T4:
    st.subheader("Логи операций (демо)")
    st.info("🚧 Логирование будет добавлено при реализации загрузки файлов")
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

