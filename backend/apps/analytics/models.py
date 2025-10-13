from django.db import models
from decimal import Decimal
from typing import Dict, Any


class ProfitabilityCalculation(models.Model):
    """Расчет прибыльности (может использоваться для кэширования)"""
    id = models.BigAutoField(primary_key=True)
    truck = models.ForeignKey(
        'trucks.Truck', 
        on_delete=models.CASCADE,
        verbose_name="Трак"
    )
    period_month = models.DateField(verbose_name="Период")
    
    # Исходные данные
    total_revenue = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Общая выручка"
    )
    total_miles = models.IntegerField(verbose_name="Общий пробег")
    
    # Переменные затраты
    salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Зарплата")
    fuel = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Топливо")
    variable_tolls = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Платные дороги (переменные)")
    
    # Фиксированные затраты (общие)
    common_ifta = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="IFTA")
    common_insurance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Общее страхование")
    common_eld = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="ELD")
    common_tablet = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Планшет")
    common_tolls = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Платные дороги (общие)")
    
    # Фиксированные затраты (по траку)
    truck_payment = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Платеж за трак")
    trailer_payment = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Платеж за прицеп")
    truck_insurance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Страхование трака")
    trailer_insurance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Страхование прицепа")
    
    # Результаты расчетов
    total_variable_costs = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Общие переменные затраты"
    )
    total_fixed_costs = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Общие фиксированные затраты"
    )
    total_costs = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Общие затраты"
    )
    profit = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Прибыль"
    )
    profit_margin = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name="Маржа прибыли (%)"
    )
    profit_per_mile = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Прибыль за милю"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'profitability_calculation'
        verbose_name = "Расчет прибыльности"
        verbose_name_plural = "Расчеты прибыльности"
        unique_together = ['truck', 'period_month']
        ordering = ['-period_month', 'truck']
    
    def __str__(self):
        return f"Расчет прибыльности {self.truck} за {self.period_month.strftime('%Y-%m')}"
    
    @classmethod
    def calculate_profitability(
        cls, 
        truck, 
        period_month, 
        variable_costs_data: Dict[str, Any],
        fixed_costs_common: Dict[str, Decimal],
        fixed_costs_truck: Dict[str, Decimal]
    ) -> 'ProfitabilityCalculation':
        """Расчет прибыльности на основе данных"""
        
        # Переменные затраты
        salary = variable_costs_data.get('salary', Decimal('0'))
        fuel = variable_costs_data.get('fuel', Decimal('0'))
        variable_tolls = variable_costs_data.get('tolls', Decimal('0'))
        total_revenue = variable_costs_data.get('total_rev', Decimal('0'))
        total_miles = variable_costs_data.get('total_miles', 0)
        
        # Общие фиксированные затраты
        common_ifta = fixed_costs_common.get('ifta', Decimal('0'))
        common_insurance = fixed_costs_common.get('insurance', Decimal('0'))
        common_eld = fixed_costs_common.get('eld', Decimal('0'))
        common_tablet = fixed_costs_common.get('tablet', Decimal('0'))
        common_tolls = fixed_costs_common.get('tolls', Decimal('0'))
        
        # Фиксированные затраты по траку
        truck_payment = fixed_costs_truck.get('truck_payment', Decimal('0'))
        trailer_payment = fixed_costs_truck.get('trailer_payment', Decimal('0'))
        truck_insurance = fixed_costs_truck.get('physical_damage_insurance_truck', Decimal('0'))
        trailer_insurance = fixed_costs_truck.get('physical_damage_insurance_trailer', Decimal('0'))
        
        # Расчеты
        total_variable_costs = salary + fuel + variable_tolls
        total_fixed_costs = (
            common_ifta + common_insurance + common_eld + common_tablet + common_tolls +
            truck_payment + trailer_payment + truck_insurance + trailer_insurance
        )
        total_costs = total_variable_costs + total_fixed_costs
        profit = total_revenue - total_costs
        
        # Процентные показатели
        profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else Decimal('0')
        profit_per_mile = profit / total_miles if total_miles > 0 else Decimal('0')
        
        return cls(
            truck=truck,
            period_month=period_month,
            total_revenue=total_revenue,
            total_miles=total_miles,
            salary=salary,
            fuel=fuel,
            variable_tolls=variable_tolls,
            common_ifta=common_ifta,
            common_insurance=common_insurance,
            common_eld=common_eld,
            common_tablet=common_tablet,
            common_tolls=common_tolls,
            truck_payment=truck_payment,
            trailer_payment=trailer_payment,
            truck_insurance=truck_insurance,
            trailer_insurance=trailer_insurance,
            total_variable_costs=total_variable_costs,
            total_fixed_costs=total_fixed_costs,
            total_costs=total_costs,
            profit=profit,
            profit_margin=profit_margin,
            profit_per_mile=profit_per_mile,
        )