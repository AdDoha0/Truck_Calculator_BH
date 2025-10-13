from rest_framework import serializers
from .models import FixedCostsCommon, FixedCostsTruck, TruckVariableCosts
from apps.trucks.models import Truck


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

