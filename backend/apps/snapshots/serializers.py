from rest_framework import serializers
from .models import CostSnapshot, CostSnapshotCommon, CostSnapshotTruck


class CostSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostSnapshot
        fields = ['id', 'snapshot_at', 'period_date', 'label']
        read_only_fields = ['id', 'snapshot_at']


class CostSnapshotCommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostSnapshotCommon
        fields = ['snapshot', 'ifta', 'insurance', 'eld', 'tablet', 'tolls']


class CostSnapshotTruckSerializer(serializers.ModelSerializer):
    truck_tractor_no = serializers.CharField(source='truck.tractor_no', read_only=True)
    
    class Meta:
        model = CostSnapshotTruck
        fields = [
            'snapshot', 'truck', 'truck_tractor_no', 'truck_payment', 'trailer_payment',
            'physical_damage_insurance_truck', 'physical_damage_insurance_trailer'
        ]


class SnapshotComparisonSerializer(serializers.Serializer):
    """Сериализатор для сравнения снимков"""
    snapshots = CostSnapshotSerializer(many=True)
    common_costs = serializers.ListField()
    truck_costs = serializers.ListField()


class CreateSnapshotSerializer(serializers.Serializer):
    """Сериализатор для создания снимка"""
    period_date = serializers.DateField()
    label = serializers.CharField(max_length=255, required=False, allow_blank=True)

