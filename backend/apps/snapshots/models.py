from django.db import models
from apps.trucks.models import Truck


class CostSnapshot(models.Model):
    """Система снимков (версии фиксированных стоимостей)"""
    id = models.BigAutoField(primary_key=True)
    snapshot_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания снимка")
    period_date = models.DateField(verbose_name="Дата периода")
    label = models.TextField(blank=True, null=True, verbose_name="Метка")
    
    class Meta:
        db_table = 'cost_snapshot'
        verbose_name = "Снимок стоимостей"
        verbose_name_plural = "Снимки стоимостей"
        ordering = ['-snapshot_at']
        # При желании можно добавить: unique_together = ['period_date']
    
    def __str__(self):
        label_text = f" ({self.label})" if self.label else ""
        return f"Снимок от {self.snapshot_at.strftime('%d.%m.%Y %H:%M:%S')}{label_text}"


class CostSnapshotCommon(models.Model):
    """Общие фиксированные стоимости в снимке"""
    snapshot = models.OneToOneField(
        CostSnapshot, 
        on_delete=models.CASCADE, 
        primary_key=True,
        verbose_name="Снимок"
    )
    ifta = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="IFTA")
    insurance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Страхование")
    eld = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="ELD")
    tablet = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Планшет")
    tolls = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Платные дороги")
    
    class Meta:
        db_table = 'cost_snapshot_common'
        verbose_name = "Общие стоимости в снимке"
        verbose_name_plural = "Общие стоимости в снимках"
    
    def __str__(self):
        return f"Общие стоимости снимка {self.snapshot.id}"


class CostSnapshotTruck(models.Model):
    """Фиксированные стоимости траков в снимке"""
    snapshot = models.ForeignKey(
        CostSnapshot, 
        on_delete=models.CASCADE,
        verbose_name="Снимок"
    )
    truck = models.ForeignKey(
        Truck, 
        on_delete=models.CASCADE,
        verbose_name="Трак"
    )
    truck_payment = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Платеж за трак"
    )
    trailer_payment = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Платеж за прицеп"
    )
    physical_damage_insurance_truck = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Страхование физического ущерба трака"
    )
    physical_damage_insurance_trailer = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Страхование физического ущерба прицепа"
    )
    
    class Meta:
        db_table = 'cost_snapshot_truck'
        verbose_name = "Стоимости трака в снимке"
        verbose_name_plural = "Стоимости траков в снимках"
        unique_together = ['snapshot', 'truck']
        indexes = [
            models.Index(fields=['truck'], name='idx_cost_snapshot_truck_truck'),
        ]
    
    def __str__(self):
        return f"{self.truck} в снимке {self.snapshot.id}"