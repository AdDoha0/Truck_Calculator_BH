from rest_framework import serializers
from datetime import date, datetime
from .models import FixedCostsCommon, FixedCostsTruck, TruckVariableCosts
from apps.trucks.models import Truck
from apps.snapshots.services import SnapshotService


class FixedCostsCommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedCostsCommon
        fields = ['id', 'ifta', 'insurance', 'eld', 'tablet', 'tolls', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class FixedCostsTruckSerializer(serializers.ModelSerializer):
    truck_tractor_no = serializers.CharField(source='truck.tractor_no', read_only=True)
    
    class Meta:
        model = FixedCostsTruck
        fields = [
            'id', 'truck', 'truck_tractor_no', 'truck_payment', 'trailer_payment',
            'physical_damage_insurance_truck', 'physical_damage_insurance_trailer',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'truck_tractor_no', 'created_at', 'updated_at']


class TruckVariableCostsSerializer(serializers.ModelSerializer):
    truck_tractor_no = serializers.CharField(source='truck.tractor_no', read_only=True)
    
    class Meta:
        model = TruckVariableCosts
        fields = [
            'id', 'period_month', 'truck', 'truck_tractor_no', 'driver_name',
            'total_rev', 'total_miles', 'salary', 'fuel', 'tolls',
            'cost_snapshot', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'truck_tractor_no', 'created_at', 'updated_at']


class TruckVariableCostsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckVariableCosts
        fields = [
            'period_month', 'truck', 'driver_name',
            'total_rev', 'total_miles', 'salary', 'fuel', 'tolls',
            'cost_snapshot'
        ]

    def validate(self, attrs):
        period = attrs.get('period_month')
        if isinstance(period, str):
            if len(period) == 7:  # YYYY-MM
                attrs['period_month'] = datetime.fromisoformat(f"{period}-01T00:00:00")
            elif len(period) == 10:  # YYYY-MM-DD
                attrs['period_month'] = datetime.fromisoformat(f"{period}T00:00:00")
        return attrs

    def create(self, validated_data):
        snapshot = validated_data.get('cost_snapshot')
        period_month = validated_data['period_month']
        if snapshot is None:
            snapshot = SnapshotService.get_latest_snapshot_for_period(period_month)
            validated_data['cost_snapshot'] = snapshot
        return super().create(validated_data)

