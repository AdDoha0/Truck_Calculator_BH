from django.contrib import admin
from .models import ProfitabilityCalculation


@admin.register(ProfitabilityCalculation)
class ProfitabilityCalculationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'truck', 'period_month', 'total_revenue', 
        'profit', 'profit_margin', 'profit_per_mile'
    ]
    list_filter = ['period_month', 'truck']
    search_fields = ['truck__tractor_no']
    ordering = ['-period_month', 'truck']
    date_hierarchy = 'period_month'
    readonly_fields = [
        'total_variable_costs', 'total_fixed_costs', 'total_costs',
        'profit', 'profit_margin', 'profit_per_mile'
    ]