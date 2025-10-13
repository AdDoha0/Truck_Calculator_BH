from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import FixedCostsCommon, FixedCostsTruck, TruckVariableCosts
from .serializers import (
    FixedCostsCommonSerializer, 
    FixedCostsTruckSerializer, 
    TruckVariableCostsSerializer,
    TruckVariableCostsCreateSerializer
)


class FixedCostsCommonViewSet(viewsets.ModelViewSet):
    queryset = FixedCostsCommon.objects.all()
    serializer_class = FixedCostsCommonSerializer
    
    def list(self, request, *args, **kwargs):
        """Получить общие фиксированные стоимости (обычно одна запись)"""
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({})
    
    def create(self, request, *args, **kwargs):
        """Создать или обновить общие фиксированные стоимости"""
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance, data=request.data)
        else:
            serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FixedCostsTruckViewSet(viewsets.ModelViewSet):
    queryset = FixedCostsTruck.objects.all()
    serializer_class = FixedCostsTruckSerializer
    
    def list(self, request, *args, **kwargs):
        """Получить фиксированные стоимости по тракам"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Создать фиксированные стоимости для трака"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TruckVariableCostsViewSet(viewsets.ModelViewSet):
    queryset = TruckVariableCosts.objects.all()
    serializer_class = TruckVariableCostsSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TruckVariableCostsCreateSerializer
        return TruckVariableCostsSerializer
    
    def list(self, request, *args, **kwargs):
        """Получить переменные затраты с фильтрацией"""
        queryset = self.get_queryset()
        
        # Фильтрация по месяцу
        period_month = request.query_params.get('period_month')
        if period_month:
            queryset = queryset.filter(period_month=period_month)
        
        # Фильтрация по траку
        truck_id = request.query_params.get('truck_id')
        if truck_id:
            queryset = queryset.filter(truck_id=truck_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Создать переменные затраты"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None, *args, **kwargs):
        """Обновить переменные затраты"""
        instance = get_object_or_404(TruckVariableCosts, pk=pk)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)