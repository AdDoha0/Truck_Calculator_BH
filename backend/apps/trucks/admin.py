from django.contrib import admin
from .models import Truck


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ['id', 'tractor_no', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['tractor_no']
    ordering = ['tractor_no']