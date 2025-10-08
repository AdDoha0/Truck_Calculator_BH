import streamlit as st
import pandas as pd
from ui_utils import inject_styles, sidebar_content
from db_utils import (
    init_database,
    create_truck,
    get_all_trucks, 
    get_truck_by_id,
    update_truck,
    delete_truck
)

st.set_page_config(page_title="Справочники • BH Trans", page_icon="📚", layout="wide")
inject_styles()
sidebar_content()

# Инициализация БД
init_database()

st.header("📚 Справочники и сервисные страницы")

T1, T2, T3 = st.tabs(["🚛 Траки", "📅 Периоды", "📋 Логи"]) 

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
    st.subheader("Загруженные периоды (демо)")
    st.info("🚧 Эта функция будет реализована при добавлении логики загрузки файлов")
    st.dataframe(pd.DataFrame({
        "period_month": ["2025-07-01","2025-08-01","2025-09-01"],
        "files": ["5/5","4/5","2/5"],
        "status": ["complete","waiting salary","waiting fuel"]
    }))

with T3:
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

