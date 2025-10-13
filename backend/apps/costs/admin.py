from django.contrib import admin
from .models import FixedCostsCommon, FixedCostsTruck, TruckVariableCosts


@admin.register(FixedCostsCommon)
class FixedCostsCommonAdmin(admin.ModelAdmin):
    list_display = ['id', 'ifta', 'insurance', 'eld', 'tablet', 'tolls', 'updated_at']
    ordering = ['-updated_at']


@admin.register(FixedCostsTruck)
class FixedCostsTruckAdmin(admin.ModelAdmin):
    list_display = ['id', 'truck', 'truck_payment', 'trailer_payment', 'updated_at']
    list_filter = ['truck']
    search_fields = ['truck__tractor_no']
    ordering = ['truck']


@admin.register(TruckVariableCosts)
class TruckVariableCostsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'truck', 'period_month', 'driver_name', 
        'total_rev', 'total_miles', 'salary', 'fuel', 'tolls'
    ]
    list_filter = ['period_month', 'truck']
    search_fields = ['truck__tractor_no', 'driver_name']
    ordering = ['-period_month', 'truck']
    date_hierarchy = 'period_month'