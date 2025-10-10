import path_setup  # This sets up the Python path

import streamlit as st
import pandas as pd
from ui_utils import sidebar_content
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
    update_common_costs,
    get_trucks_full_data,
    get_available_periods
)

st.set_page_config(page_title="Справочники • BH Trans", page_icon="📚", layout="wide")
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
    
    # ========== ПРОДВИНУТАЯ ТАБЛИЦА ТРАКОВ ==========
    st.markdown("### 📋 Продвинутая таблица управления траками")
    
    # Инициализация session_state для периода
    if 'selected_period' not in st.session_state:
        st.session_state.selected_period = None
    
    # Callback функция для обновления при смене периода
    def on_period_change():
        # При изменении периода очищаем кеш таблицы
        if 'trucks_table_data' in st.session_state:
            del st.session_state.trucks_table_data
    
    # Выбор периода для отображения переменных расходов
    col_period, col_info = st.columns([3, 1])
    
    with col_period:
        available_periods = get_available_periods()
        
        if available_periods:
            selected_period = st.selectbox(
                "Выберите период для отображения переменных расходов",
                options=available_periods,
                help="Выберите месяц для загрузки переменных расходов",
                key="period_selector",
                on_change=on_period_change,
                index=0 if st.session_state.selected_period is None else (
                    available_periods.index(st.session_state.selected_period) 
                    if st.session_state.selected_period in available_periods 
                    else 0
                )
            )
            
            # Сохраняем в session_state
            st.session_state.selected_period = selected_period
            
            # Показываем выбранный период для отладки
            st.caption(f"📅 Загружаются данные за: **{selected_period}**")
        else:
            st.info("📭 Нет загруженных месячных данных. Переменные расходы будут равны 0.")
            selected_period = None
            st.session_state.selected_period = None
    
    with col_info:
        st.markdown("**Легенда:**")
        st.caption("🔵 Фикс. расходы")
        st.caption("🟢 Перем. расходы")
    
    # Получаем данные траков с расходами - явно передаём период
    trucks_data = get_trucks_full_data(selected_period if selected_period else None)
    
    if not trucks_data:
        st.info("📭 Траки не найдены. Добавьте первый трак выше.")
    else:
        # Debug: показываем сколько траков с месячными данными
        trucks_with_data = len([t for t in trucks_data if t.get('has_monthly_data', False)])
        
        # Debug панель с подробной информацией
        if selected_period:
            debug_col1, debug_col2 = st.columns([2, 1])
            
            with debug_col1:
                st.info(f"ℹ️ Траков с данными за выбранный период: **{trucks_with_data}** из {len(trucks_data)}")
            
            with debug_col2:
                # Показываем пример данных первого трака с данными
                first_truck_with_data = next((t for t in trucks_data if t.get('has_monthly_data', False)), None)
                if first_truck_with_data:
                    with st.expander("🔍 Пример данных (DEBUG)"):
                        st.write(f"**Трак:** {first_truck_with_data['tractor_no']}")
                        st.write(f"**Зарплата:** ${first_truck_with_data['salary']:.2f}")
                        st.write(f"**Топливо:** ${first_truck_with_data['fuel']:.2f}")
                        st.write(f"**Сборы:** ${first_truck_with_data['tolls']:.2f}")
        
        # Подготовка данных для таблицы
        table_data = []
        for truck in trucks_data:
            # Вычисляем итоги
            total_fixed = (truck['truck_payment'] + truck['trailer_payment'] + 
                          truck['truck_insurance'] + truck['trailer_insurance'])
            total_variable = (truck['salary'] + truck['fuel'] + truck['tolls'])
            total_all = total_fixed + total_variable
            
            table_data.append({
                'ID': truck['id'],
                'Номер трака': truck['tractor_no'],
                # Фиксированные расходы
                '💰 Выплата трак': truck['truck_payment'],
                '💰 Выплата прицеп': truck['trailer_payment'],
                '🛡️ Страх. трак': truck['truck_insurance'],
                '🛡️ Страх. прицеп': truck['trailer_insurance'],
                '📊 ИТОГО ФИКС': total_fixed,
                # Переменные расходы
                '👷 Зарплата': truck['salary'],
                '⛽ Топливо': truck['fuel'],
                '🛣️ Дор. сборы': truck['tolls'],
                '📊 ИТОГО ПЕРЕМ': total_variable,
                # Общий итог
                '💵 ВСЕГО': total_all,
            })
        
        df = pd.DataFrame(table_data)
        
        # Настройка колонок для редактирования
        column_config = {
            'ID': st.column_config.NumberColumn('ID', disabled=True, width='small'),
            'Номер трака': st.column_config.TextColumn('Номер трака', disabled=True, width='medium'),
            # Фиксированные расходы - редактируемые
            '💰 Выплата трак': st.column_config.NumberColumn('💰 Выплата трак', min_value=0, format='$%.2f'),
            '💰 Выплата прицеп': st.column_config.NumberColumn('💰 Выплата прицеп', min_value=0, format='$%.2f'),
            '🛡️ Страх. трак': st.column_config.NumberColumn('🛡️ Страх. трак', min_value=0, format='$%.2f'),
            '🛡️ Страх. прицеп': st.column_config.NumberColumn('🛡️ Страх. прицеп', min_value=0, format='$%.2f'),
            '📊 ИТОГО ФИКС': st.column_config.NumberColumn('📊 ИТОГО ФИКС', disabled=True, format='$%.2f'),
            # Переменные расходы - редактируемые если выбран период
            '👷 Зарплата': st.column_config.NumberColumn('👷 Зарплата', min_value=0, format='$%.2f', disabled=(selected_period is None)),
            '⛽ Топливо': st.column_config.NumberColumn('⛽ Топливо', min_value=0, format='$%.2f', disabled=(selected_period is None)),
            '🛣️ Дор. сборы': st.column_config.NumberColumn('🛣️ Дор. сборы', min_value=0, format='$%.2f', disabled=(selected_period is None)),
            '📊 ИТОГО ПЕРЕМ': st.column_config.NumberColumn('📊 ИТОГО ПЕРЕМ', disabled=True, format='$%.2f'),
            # Общий итог
            '💵 ВСЕГО': st.column_config.NumberColumn('💵 ВСЕГО', disabled=True, format='$%.2f', width='medium'),
        }
        
        # Отображение редактируемой таблицы
        # Key зависит от периода, чтобы таблица обновлялась при смене периода
        table_key = f"trucks_table_editor_{selected_period}" if selected_period else "trucks_table_editor_no_period"
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            column_config=column_config,
            key=table_key
        )
        
        # Обработка изменений
        if not df.equals(edited_df):
            st.markdown("### 🔄 Обнаружены изменения")
            
            # Найти изменённые строки
            changes_detected = False
            
            for idx in range(len(df)):
                truck_id = int(df.iloc[idx]['ID'])
                original_row = df.iloc[idx]
                edited_row = edited_df.iloc[idx]
                
                # Проверка изменений в фиксированных расходах
                fixed_costs_changed = (
                    original_row['💰 Выплата трак'] != edited_row['💰 Выплата трак'] or
                    original_row['💰 Выплата прицеп'] != edited_row['💰 Выплата прицеп'] or
                    original_row['🛡️ Страх. трак'] != edited_row['🛡️ Страх. трак'] or
                    original_row['🛡️ Страх. прицеп'] != edited_row['🛡️ Страх. прицеп']
                )
                
                # Проверка изменений в переменных расходах
                variable_costs_changed = selected_period and (
                    original_row['👷 Зарплата'] != edited_row['👷 Зарплата'] or
                    original_row['⛽ Топливо'] != edited_row['⛽ Топливо'] or
                    original_row['🛣️ Дор. сборы'] != edited_row['🛣️ Дор. сборы']
                )
                
                if fixed_costs_changed:
                    changes_detected = True
                    st.info(f"Обновление фикс. расходов для трака ID {truck_id}...")
                    update_truck_costs(
                        truck_id,
                        truck_payment=float(edited_row['💰 Выплата трак']),
                        trailer_payment=float(edited_row['💰 Выплата прицеп']),
                        physical_damage_insurance_truck=float(edited_row['🛡️ Страх. трак']),
                        physical_damage_insurance_trailer=float(edited_row['🛡️ Страх. прицеп'])
                    )
                
                if variable_costs_changed:
                    changes_detected = True
                    st.info(f"⚠️ Переменные расходы обновляются через загрузку Excel файлов (страница Upload)")
                    # Note: Variable costs are now managed through Excel upload process
            
            if changes_detected:
                st.success("✅ Все изменения сохранены! Перезагрузите страницу для обновления.")
                if st.button("🔄 Перезагрузить данные"):
                    st.rerun()
        
        st.markdown(f"**Всего траков:** {len(trucks_data)}")
        
        # ========== РЕДАКТИРОВАНИЕ/УДАЛЕНИЕ ТРАКА ==========
        st.divider()
        st.markdown("### ✏️ Редактировать/Удалить трак")
        
        truck_options = {f"{truck['tractor_no']} (ID: {truck['id']})": truck['id'] 
                        for truck in trucks_data}
        
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
                    # Форма редактирования номера трака
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

