from rest_framework import serializers
from .models import Truck


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ['id', 'tractor_no', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TruckCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ['tractor_no']

