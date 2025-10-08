import streamlit as st
import pandas as pd
from ui_utils import inject_styles, sidebar_content
from db_utils import (
    init_database,
    get_common_fixed_costs,
    save_common_fixed_costs,
    get_trucks_list_for_selectbox,
    get_truck_fixed_costs,
    save_truck_fixed_costs,
    delete_truck_fixed_costs,
    get_all_trucks
)

st.set_page_config(page_title="Настройки • BH Trans", page_icon="⚙️", layout="wide")
inject_styles()
sidebar_content()

# Инициализация БД
init_database()

st.header("⚙️ Настройки фиксированных расходов")

c_common, c_truck = st.tabs(["🌐 Общие расходы", "🚛 Индивидуальные расходы"])

with c_common:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Общие фиксированные расходы для всех траков")
    st.markdown("*Эти расходы применяются ко всем тракам ежемесячно*")
    
    # Загружаем текущие значения из БД
    current_costs = get_common_fixed_costs()
    
    if current_costs:
        with st.form("common_costs_form"):
            st.markdown("#### 💰 Настройка расходов")
            
            col1, col2 = st.columns(2)
            with col1:
                ifta = st.number_input(
                    "IFTA ($/мес)", 
                    min_value=0.0, 
                    value=float(current_costs['ifta']), 
                    step=10.0,
                    help="International Fuel Tax Agreement - налог на топливо"
                )
                insurance = st.number_input(
                    "Страховка Liability ($/мес)", 
                    min_value=0.0, 
                    value=float(current_costs['insurance']), 
                    step=10.0,
                    help="Обязательное страхование ответственности"
                )
                tolls = st.number_input(
                    "Платные дороги ($/мес)", 
                    min_value=0.0, 
                    value=float(current_costs['tolls']), 
                    step=5.0,
                    help="Базовая подписка на систему оплаты платных дорог"
                )
            
            with col2:
                eld = st.number_input(
                    "ELD система ($/мес)", 
                    min_value=0.0, 
                    value=float(current_costs['eld']), 
                    step=1.0,
                    help="Electronic Logging Device - электронные логбуки"
                )
                tablet = st.number_input(
                    "Планшеты ($/мес)", 
                    min_value=0.0, 
                    value=float(current_costs['tablet']), 
                    step=1.0,
                    help="Планшеты для водителей"
                )
            
            # Показываем общую сумму
            total_common = ifta + insurance + eld + tablet + tolls
            st.markdown(f"**📊 Общая сумма:** ${total_common:.2f} в месяц")
            
            submit_common = st.form_submit_button("💾 Сохранить общие расходы", type="primary")
            
            if submit_common:
                if save_common_fixed_costs(ifta, insurance, eld, tablet, tolls):
                    st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

with c_truck:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Индивидуальные фиксированные расходы по тракам")
    st.markdown("*Эти расходы привязаны к конкретному траку*")
    
    # Получаем список траков
    trucks = get_all_trucks()
    
    if not trucks:
        st.info("📭 Сначала добавьте траки в разделе 'Справочники' → 'Траки'")
    else:
        # Выбор трака
        truck_options = {f"{truck['tractor_no']} (ID: {truck['id']})": truck['id'] 
                        for truck in trucks}
        
        selected_truck_label = st.selectbox(
            "🚛 Выберите трак",
            options=list(truck_options.keys()),
            help="Выберите трак для настройки индивидуальных расходов"
        )
        
        if selected_truck_label:
            selected_truck_id = truck_options[selected_truck_label]
            selected_truck_no = selected_truck_label.split(" (ID:")[0]
            
            # Загружаем текущие расходы для выбранного трака
            truck_costs = get_truck_fixed_costs(selected_truck_id)
            
            if truck_costs:
                col_form, col_info = st.columns([2, 1])
                
                with col_form:
                    with st.form(f"truck_costs_form_{selected_truck_id}"):
                        st.markdown(f"#### 💰 Настройка расходов для трака **{selected_truck_no}**")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            truck_payment = st.number_input(
                                "Платёж по траку ($/мес)", 
                                min_value=0.0, 
                                value=float(truck_costs['truck_payment']), 
                                step=10.0,
                                help="Ежемесячный платёж за трак (лизинг/кредит)"
                            )
                            pd_truck = st.number_input(
                                "Страховка PD трак ($/мес)", 
                                min_value=0.0, 
                                value=float(truck_costs['physical_damage_insurance_truck']), 
                                step=10.0,
                                help="Physical Damage Insurance для трака"
                            )
                        
                        with col2:
                            trailer_payment = st.number_input(
                                "Платёж по прицепу ($/мес)", 
                                min_value=0.0, 
                                value=float(truck_costs['trailer_payment']), 
                                step=10.0,
                                help="Ежемесячный платёж за прицеп (лизинг/кредит)"
                            )
                            pd_trailer = st.number_input(
                                "Страховка PD прицеп ($/мес)", 
                                min_value=0.0, 
                                value=float(truck_costs['physical_damage_insurance_trailer']), 
                                step=10.0,
                                help="Physical Damage Insurance для прицепа"
                            )
                        
                        # Показываем общую сумму
                        total_truck = truck_payment + trailer_payment + pd_truck + pd_trailer
                        st.markdown(f"**📊 Сумма для трака {selected_truck_no}:** ${total_truck:.2f} в месяц")
                        
                        submit_truck = st.form_submit_button("💾 Сохранить расходы трака", type="primary")
                        
                        if submit_truck:
                            if save_truck_fixed_costs(selected_truck_id, truck_payment, trailer_payment, pd_truck, pd_trailer):
                                st.rerun()
                
                with col_info:
                    st.markdown("#### 📋 Действия")
                    
                    # Показываем информацию о текущих расходах
                    if any([truck_costs['truck_payment'], truck_costs['trailer_payment'], 
                           truck_costs['physical_damage_insurance_truck'], truck_costs['physical_damage_insurance_trailer']]):
                        st.markdown("**Текущие расходы:**")
                        if truck_costs['truck_payment'] > 0:
                            st.write(f"• Трак: ${truck_costs['truck_payment']:.2f}")
                        if truck_costs['trailer_payment'] > 0:
                            st.write(f"• Прицеп: ${truck_costs['trailer_payment']:.2f}")
                        if truck_costs['physical_damage_insurance_truck'] > 0:
                            st.write(f"• PD трак: ${truck_costs['physical_damage_insurance_truck']:.2f}")
                        if truck_costs['physical_damage_insurance_trailer'] > 0:
                            st.write(f"• PD прицеп: ${truck_costs['physical_damage_insurance_trailer']:.2f}")
                        
                        st.divider()
                        
                        # Кнопка удаления расходов
                        if st.button("🗑️ Очистить все расходы", 
                                   key=f"delete_costs_{selected_truck_id}",
                                   help="Удалить все фиксированные расходы для этого трака"):
                            if delete_truck_fixed_costs(selected_truck_id):
                                st.rerun()
                    else:
                        st.info("Расходы для этого трака ещё не настроены")
        
        # Показываем сводку по всем тракам
        st.divider()
        st.markdown("#### 📊 Сводка по всем тракам")
        
        trucks_summary = []
        for truck in trucks:
            truck_costs = get_truck_fixed_costs(truck['id'])
            if truck_costs:
                total = (truck_costs['truck_payment'] + truck_costs['trailer_payment'] + 
                        truck_costs['physical_damage_insurance_truck'] + truck_costs['physical_damage_insurance_trailer'])
                trucks_summary.append({
                    "Трак": truck['tractor_no'],
                    "Платёж трак": f"${truck_costs['truck_payment']:.2f}",
                    "Платёж прицеп": f"${truck_costs['trailer_payment']:.2f}",
                    "PD трак": f"${truck_costs['physical_damage_insurance_truck']:.2f}",
                    "PD прицеп": f"${truck_costs['physical_damage_insurance_trailer']:.2f}",
                    "Всего": f"${total:.2f}"
                })
        
        if trucks_summary:
            df_summary = pd.DataFrame(trucks_summary)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
        else:
            st.info("Индивидуальные расходы ещё не настроены ни для одного трака")
    
    st.markdown("</div>", unsafe_allow_html=True)

