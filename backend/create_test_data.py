#!/usr/bin/env python
"""
Скрипт для создания тестовых данных в базе данных
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Добавляем путь к проекту
sys.path.append('/home/user/my_projects/BH/truck_calculate/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.trucks.models import Truck
from apps.costs.models import (
    FixedCostsCommon, 
    FixedCostsTruck, 
    TruckVariableCosts
)

def create_test_data():
    print("Создание тестовых данных...")
    
    # 1. Создаем общие фиксированные затраты
    print("Создание общих фиксированных затрат...")
    common_costs, created = FixedCostsCommon.objects.get_or_create(
        defaults={
            'ifta': Decimal('500.00'),
            'insurance': Decimal('800.00'),
            'eld': Decimal('300.00'),
            'tablet': Decimal('200.00'),
            'tolls': Decimal('600.00'),
        }
    )
    print(f"Общие затраты: {'созданы' if created else 'уже существуют'}")
    
    # 2. Создаем траки
    print("Создание траков...")
    trucks_data = [
        {
            'tractor_no': 'TR-001',
            'tractor_model': 'Volvo FH16',
            'tractor_year': 2020,
            'tractor_mileage': 150000,
            'trailer_no': 'TRL-001',
            'trailer_model': 'Schmitz SCF',
            'trailer_year': 2019,
            'trailer_mileage': 120000,
            'is_active': True,
        },
        {
            'tractor_no': 'TR-002',
            'tractor_model': 'Scania R500',
            'tractor_year': 2021,
            'tractor_mileage': 80000,
            'trailer_no': 'TRL-002',
            'trailer_model': 'Krone ProfiLiner',
            'trailer_year': 2020,
            'trailer_mileage': 90000,
            'is_active': True,
        },
        {
            'tractor_no': 'TR-003',
            'tractor_model': 'Mercedes Actros',
            'tractor_year': 2019,
            'tractor_mileage': 200000,
            'trailer_no': 'TRL-003',
            'trailer_model': 'Krone CoolLiner',
            'trailer_year': 2018,
            'trailer_mileage': 180000,
            'is_active': True,
        },
        {
            'tractor_no': 'TR-004',
            'tractor_model': 'MAN TGX',
            'tractor_year': 2022,
            'tractor_mileage': 50000,
            'trailer_no': 'TRL-004',
            'trailer_model': 'Schmitz S.KO',
            'trailer_year': 2021,
            'trailer_mileage': 45000,
            'is_active': False,
        },
    ]
    
    trucks = []
    for truck_data in trucks_data:
        truck, created = Truck.objects.get_or_create(
            tractor_no=truck_data['tractor_no'],
            defaults=truck_data
        )
        trucks.append(truck)
        print(f"Трак {truck.tractor_no}: {'создан' if created else 'уже существует'}")
    
    # 3. Создаем фиксированные затраты для траков
    print("Создание фиксированных затрат для траков...")
    fixed_costs_data = [
        {
            'truck': trucks[0],
            'truck_payment': Decimal('2500.00'),
            'trailer_payment': Decimal('800.00'),
            'physical_damage_insurance_truck': Decimal('300.00'),
            'physical_damage_insurance_trailer': Decimal('150.00'),
        },
        {
            'truck': trucks[1],
            'truck_payment': Decimal('2800.00'),
            'trailer_payment': Decimal('900.00'),
            'physical_damage_insurance_truck': Decimal('350.00'),
            'physical_damage_insurance_trailer': Decimal('180.00'),
        },
        {
            'truck': trucks[2],
            'truck_payment': Decimal('2200.00'),
            'trailer_payment': Decimal('750.00'),
            'physical_damage_insurance_truck': Decimal('280.00'),
            'physical_damage_insurance_trailer': Decimal('140.00'),
        },
        {
            'truck': trucks[3],
            'truck_payment': Decimal('3000.00'),
            'trailer_payment': Decimal('950.00'),
            'physical_damage_insurance_truck': Decimal('400.00'),
            'physical_damage_insurance_trailer': Decimal('200.00'),
        },
    ]
    
    for cost_data in fixed_costs_data:
        fixed_cost, created = FixedCostsTruck.objects.get_or_create(
            truck=cost_data['truck'],
            defaults=cost_data
        )
        print(f"Фиксированные затраты для {cost_data['truck'].tractor_no}: {'созданы' if created else 'уже существуют'}")
    
    # 4. Создаем переменные затраты для разных периодов
    print("Создание переменных затрат для разных периодов...")
    
    # Создаем периоды за последние 6 месяцев
    base_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    periods = []
    for i in range(6):
        period_date = base_date - timedelta(days=30 * i)
        periods.append(period_date)
    
    # Данные для переменных затрат по тракам и периодам
    variable_costs_data = [
        # TR-001 данные
        {
            'truck': trucks[0],
            'period_month': periods[0],  # Текущий месяц
            'driver_name': 'Иван Петров',
            'total_rev': Decimal('15000.00'),
            'total_miles': 4500,
            'salary': Decimal('3000.00'),
            'fuel': Decimal('1200.00'),
            'tolls': Decimal('150.00'),
        },
        {
            'truck': trucks[0],
            'period_month': periods[1],  # Предыдущий месяц
            'driver_name': 'Иван Петров',
            'fuel_cost': Decimal('1150.00'),
            'toll_cost': Decimal('140.00'),
            'parking_cost': Decimal('75.00'),
            'maintenance_cost': Decimal('180.00'),
            'repair_cost': Decimal('120.00'),
            'tire_cost': Decimal('280.00'),
            'other_cost': Decimal('90.00'),
        },
        {
            'truck': trucks[0],
            'period_month': periods[2],  # 2 месяца назад
            'driver_name': 'Сергей Сидоров',
            'fuel_cost': Decimal('1300.00'),
            'toll_cost': Decimal('160.00'),
            'parking_cost': Decimal('85.00'),
            'maintenance_cost': Decimal('220.00'),
            'repair_cost': Decimal('180.00'),
            'tire_cost': Decimal('320.00'),
            'other_cost': Decimal('110.00'),
        },
        
        # TR-002 данные
        {
            'truck': trucks[1],
            'period_month': periods[0],
            'driver_name': 'Алексей Козлов',
            'fuel_cost': Decimal('1100.00'),
            'toll_cost': Decimal('130.00'),
            'parking_cost': Decimal('70.00'),
            'maintenance_cost': Decimal('190.00'),
            'repair_cost': Decimal('100.00'),
            'tire_cost': Decimal('250.00'),
            'other_cost': Decimal('80.00'),
        },
        {
            'truck': trucks[1],
            'period_month': periods[1],
            'driver_name': 'Алексей Козлов',
            'fuel_cost': Decimal('1050.00'),
            'toll_cost': Decimal('125.00'),
            'parking_cost': Decimal('65.00'),
            'maintenance_cost': Decimal('170.00'),
            'repair_cost': Decimal('90.00'),
            'tire_cost': Decimal('230.00'),
            'other_cost': Decimal('75.00'),
        },
        {
            'truck': trucks[1],
            'period_month': periods[3],  # 3 месяца назад
            'driver_name': 'Михаил Волков',
            'fuel_cost': Decimal('1250.00'),
            'toll_cost': Decimal('145.00'),
            'parking_cost': Decimal('80.00'),
            'maintenance_cost': Decimal('210.00'),
            'repair_cost': Decimal('160.00'),
            'tire_cost': Decimal('290.00'),
            'other_cost': Decimal('95.00'),
        },
        
        # TR-003 данные
        {
            'truck': trucks[2],
            'period_month': periods[0],
            'driver_name': 'Дмитрий Соколов',
            'fuel_cost': Decimal('1400.00'),
            'toll_cost': Decimal('180.00'),
            'parking_cost': Decimal('95.00'),
            'maintenance_cost': Decimal('250.00'),
            'repair_cost': Decimal('200.00'),
            'tire_cost': Decimal('350.00'),
            'other_cost': Decimal('120.00'),
        },
        {
            'truck': trucks[2],
            'period_month': periods[1],
            'driver_name': 'Дмитрий Соколов',
            'fuel_cost': Decimal('1350.00'),
            'toll_cost': Decimal('170.00'),
            'parking_cost': Decimal('90.00'),
            'maintenance_cost': Decimal('230.00'),
            'repair_cost': Decimal('180.00'),
            'tire_cost': Decimal('330.00'),
            'other_cost': Decimal('110.00'),
        },
        {
            'truck': trucks[2],
            'period_month': periods[2],
            'driver_name': 'Андрей Морозов',
            'fuel_cost': Decimal('1450.00'),
            'toll_cost': Decimal('190.00'),
            'parking_cost': Decimal('100.00'),
            'maintenance_cost': Decimal('270.00'),
            'repair_cost': Decimal('220.00'),
            'tire_cost': Decimal('370.00'),
            'other_cost': Decimal('130.00'),
        },
        {
            'truck': trucks[2],
            'period_month': periods[4],  # 4 месяца назад
            'driver_name': 'Андрей Морозов',
            'fuel_cost': Decimal('1500.00'),
            'toll_cost': Decimal('200.00'),
            'parking_cost': Decimal('105.00'),
            'maintenance_cost': Decimal('290.00'),
            'repair_cost': Decimal('240.00'),
            'tire_cost': Decimal('390.00'),
            'other_cost': Decimal('140.00'),
        },
        
        # TR-004 данные (неактивный трак)
        {
            'truck': trucks[3],
            'period_month': periods[5],  # 5 месяцев назад
            'driver_name': 'Владимир Лебедев',
            'fuel_cost': Decimal('1000.00'),
            'toll_cost': Decimal('120.00'),
            'parking_cost': Decimal('60.00'),
            'maintenance_cost': Decimal('150.00'),
            'repair_cost': Decimal('80.00'),
            'tire_cost': Decimal('200.00'),
            'other_cost': Decimal('70.00'),
        },
    ]
    
    for cost_data in variable_costs_data:
        variable_cost, created = TruckVariableCosts.objects.get_or_create(
            truck=cost_data['truck'],
            period_month=cost_data['period_month'],
            defaults=cost_data
        )
        print(f"Переменные затраты для {cost_data['truck'].tractor_no} за {cost_data['period_month'].strftime('%Y-%m-%d')}: {'созданы' if created else 'уже существуют'}")
    
    print("\n✅ Тестовые данные успешно созданы!")
    print(f"Создано траков: {Truck.objects.count()}")
    print(f"Создано фиксированных затрат: {FixedCostsTruck.objects.count()}")
    print(f"Создано переменных затрат: {TruckVariableCosts.objects.count()}")
    print(f"Создано общих затрат: {FixedCostsCommon.objects.count()}")
    
    # Выводим информацию о периодах
    print("\n📅 Доступные периоды:")
    periods = TruckVariableCosts.objects.values_list('period_month', flat=True).distinct().order_by('-period_month')
    for period in periods:
        print(f"  - {period.strftime('%d %B %Y г.')}")

if __name__ == '__main__':
    create_test_data()
