from rest_framework import serializers
from datetime import date, datetime
from .models import FixedCostsCommon, FixedCostsTruck, TruckVariableCosts, TruckCurrentVariableCosts
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
            'id', 'snapshot', 'truck', 'truck_tractor_no', 'driver_name',
            'total_rev', 'total_miles', 'salary', 'fuel', 'tolls',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'truck_tractor_no', 'created_at', 'updated_at']


class TruckVariableCostsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckVariableCosts
        fields = [
            'snapshot', 'truck', 'driver_name',
            'total_rev', 'total_miles', 'salary', 'fuel', 'tolls'
        ]
    # никаких периодов: привязка только через snapshot


class TruckCurrentVariableCostsSerializer(serializers.ModelSerializer):
    truck_tractor_no = serializers.CharField(source='truck.tractor_no', read_only=True)
    
    class Meta:
        model = TruckCurrentVariableCosts
        fields = [
            'id', 'truck', 'truck_tractor_no', 'driver_name',
            'total_rev', 'total_miles', 'salary', 'fuel', 'tolls',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'truck_tractor_no', 'created_at', 'updated_at']


class TruckCurrentVariableCostsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckCurrentVariableCosts
        fields = [
            'truck', 'driver_name', 'total_rev', 'total_miles', 
            'salary', 'fuel', 'tolls'
        ]

