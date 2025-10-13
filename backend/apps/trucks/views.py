from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Truck
from .serializers import TruckSerializer, TruckCreateSerializer
from apps.costs.models import FixedCostsTruck, TruckVariableCosts
from apps.costs.serializers import FixedCostsTruckSerializer, TruckVariableCostsSerializer


class TruckViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TruckCreateSerializer
        return TruckSerializer
    
    def list(self, request, *args, **kwargs):
        """Получить список всех траков"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Создать новый трак"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            truck = serializer.save()
            return Response(
                TruckSerializer(truck).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        """Получить конкретный трак"""
        truck = get_object_or_404(Truck, pk=pk)
        serializer = self.get_serializer(truck)
        return Response(serializer.data)
    
    def update(self, request, pk=None, *args, **kwargs):
        """Обновить трак"""
        truck = get_object_or_404(Truck, pk=pk)
        serializer = self.get_serializer(truck, data=request.data)
        if serializer.is_valid():
            truck = serializer.save()
            return Response(TruckSerializer(truck).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        """Удалить трак"""
        truck = get_object_or_404(Truck, pk=pk)
        truck.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'], url_path='full-details')
    def full_details(self, request, pk=None):
        """Получить полную информацию о траке включая все затраты"""
        truck = get_object_or_404(Truck, pk=pk)
        truck_data = TruckSerializer(truck).data
        
        # Получить фиксированные затраты
        try:
            fixed_costs = FixedCostsTruck.objects.get(truck_id=pk)
            truck_data['fixed_costs'] = FixedCostsTruckSerializer(fixed_costs).data
        except FixedCostsTruck.DoesNotExist:
            truck_data['fixed_costs'] = None
        
        # Получить переменные затраты
        variable_costs = TruckVariableCosts.objects.filter(truck_id=pk).order_by('-period_month')
        truck_data['variable_costs'] = TruckVariableCostsSerializer(variable_costs, many=True).data
        
        return Response(truck_data)