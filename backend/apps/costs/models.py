from django.db import models
from apps.trucks.models import Truck


class FixedCostsCommon(models.Model):
    """Общие фиксированные стоимости"""
    id = models.BigAutoField(primary_key=True)
    ifta = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="IFTA")
    insurance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Страхование")
    eld = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="ELD")
    tablet = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Планшет")
    tolls = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Платные дороги")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'fixed_costs_common'
        verbose_name = "Общие фиксированные стоимости"
        verbose_name_plural = "Общие фиксированные стоимости"
    
    def __str__(self):
        return f"Общие фиксированные стоимости (ID: {self.id})"


class FixedCostsTruck(models.Model):
    """Фиксированные стоимости по тракам"""
    id = models.BigAutoField(primary_key=True)
    truck = models.ForeignKey(
        Truck, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Трак"
    )
    truck_payment = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Платеж за трак"
    )
    trailer_payment = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Платеж за прицеп"
    )
    physical_damage_insurance_truck = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Страхование физического ущерба трака"
    )
    physical_damage_insurance_trailer = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Страхование физического ущерба прицепа"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'fixed_costs_truck'
        verbose_name = "Фиксированные стоимости трака"
        verbose_name_plural = "Фиксированные стоимости траков"
        unique_together = ['truck']
    
    def __str__(self):
        return f"Фиксированные стоимости для {self.truck}"


class TruckVariableCosts(models.Model):
    """Переменные (нефиксированные) данные по тракам"""
    id = models.BigAutoField(primary_key=True)
    period_month = models.DateField(verbose_name="Период (месяц)")
    truck = models.ForeignKey(
        Truck, 
        on_delete=models.CASCADE, 
        verbose_name="Трак"
    )
    
    driver_name = models.TextField(blank=True, null=True, verbose_name="Имя водителя")
    total_rev = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Общая выручка"
    )
    total_miles = models.IntegerField(default=0, verbose_name="Общий пробег")
    salary = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Зарплата"
    )
    fuel = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Топливо"
    )
    tolls = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0, 
        verbose_name="Платные дороги"
    )
    
    # Привязка к снимку фикс-стоимостей
    cost_snapshot = models.ForeignKey(
        'snapshots.CostSnapshot', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Снимок фиксированных стоимостей"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'truck_variable_costs'
        verbose_name = "Переменные затраты трака"
        verbose_name_plural = "Переменные затраты траков"
        unique_together = ['period_month', 'truck']
        ordering = ['-period_month', 'truck']
    
    def __str__(self):
        return f"{self.truck} - {self.period_month.strftime('%Y-%m')}"