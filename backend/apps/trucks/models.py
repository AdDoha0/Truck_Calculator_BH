from django.db import models


class Truck(models.Model):
    """Модель трака"""
    id = models.AutoField(primary_key=True)
    tractor_no = models.TextField(unique=True, verbose_name="Номер трактора")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'truck'
        verbose_name = "Трак"
        verbose_name_plural = "Траки"
        ordering = ['tractor_no']
    
    def __str__(self):
        return f"Трак {self.tractor_no}"