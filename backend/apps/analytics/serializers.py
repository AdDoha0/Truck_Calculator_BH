from rest_framework import serializers
from .models import ProfitabilityCalculation


class ProfitabilityCalculationSerializer(serializers.ModelSerializer):
    truck_tractor_no = serializers.CharField(source='truck.tractor_no', read_only=True)
    
    class Meta:
        model = ProfitabilityCalculation
        fields = [
            'id', 'truck', 'truck_tractor_no', 'period_month',
            'total_revenue', 'total_miles', 'salary', 'fuel', 'variable_tolls',
            'common_ifta', 'common_insurance', 'common_eld', 'common_tablet', 'common_tolls',
            'truck_payment', 'trailer_payment', 'truck_insurance', 'trailer_insurance',
            'total_variable_costs', 'total_fixed_costs', 'total_costs',
            'profit', 'profit_margin', 'profit_per_mile',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'truck_tractor_no', 'total_variable_costs', 'total_fixed_costs',
            'total_costs', 'profit', 'profit_margin', 'profit_per_mile',
            'created_at', 'updated_at'
        ]


class ProfitabilitySummarySerializer(serializers.Serializer):
    """Сериализатор для сводки по прибыльности"""
    total_trucks = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_costs = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_profit_margin = serializers.DecimalField(max_digits=5, decimal_places=2)
    period_month = serializers.DateField()


class TruckProfitabilitySerializer(serializers.Serializer):
    """Сериализатор для прибыльности по тракам"""
    truck_id = serializers.IntegerField()
    truck_tractor_no = serializers.CharField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_costs = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit_margin = serializers.DecimalField(max_digits=5, decimal_places=2)
    profit_per_mile = serializers.DecimalField(max_digits=12, decimal_places=2)

