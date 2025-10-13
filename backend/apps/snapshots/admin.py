from django.contrib import admin
from .models import CostSnapshot, CostSnapshotCommon, CostSnapshotTruck


class CostSnapshotTruckInline(admin.TabularInline):
    model = CostSnapshotTruck
    extra = 0


@admin.register(CostSnapshot)
class CostSnapshotAdmin(admin.ModelAdmin):
    list_display = ['id', 'snapshot_at', 'period_date', 'label']
    list_filter = ['period_date', 'snapshot_at']
    search_fields = ['label']
    ordering = ['-snapshot_at']
    date_hierarchy = 'snapshot_at'
    inlines = [CostSnapshotTruckInline]


@admin.register(CostSnapshotCommon)
class CostSnapshotCommonAdmin(admin.ModelAdmin):
    list_display = ['snapshot', 'ifta', 'insurance', 'eld', 'tablet', 'tolls']
    list_filter = ['snapshot__period_date']


@admin.register(CostSnapshotTruck)
class CostSnapshotTruckAdmin(admin.ModelAdmin):
    list_display = ['snapshot', 'truck', 'truck_payment', 'trailer_payment']
    list_filter = ['snapshot', 'truck']
    search_fields = ['truck__tractor_no']
    ordering = ['snapshot', 'truck']