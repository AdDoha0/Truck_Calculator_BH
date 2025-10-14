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
        
        # Фильтрация по траку
        truck_id = request.query_params.get('truck_id')
        if truck_id:
            queryset = queryset.filter(truck_id=truck_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Создать фиксированные стоимости для трака"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='by-truck/(?P<truck_id>[^/.]+)')
    def by_truck(self, request, truck_id=None):
        """Получить фиксированные затраты для конкретного трака"""
        try:
            fixed_costs = FixedCostsTruck.objects.get(truck_id=truck_id)
            serializer = self.get_serializer(fixed_costs)
            return Response(serializer.data)
        except FixedCostsTruck.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK)


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
            # Если period_month приходит как массив, берем первый элемент
            if isinstance(period_month, list):
                period_month = period_month[0]
            
            # Обрабатываем различные форматы дат
            if len(period_month) == 7:  # YYYY-MM формат
                period_month = f"{period_month}-01T00:00:00"
            elif len(period_month) == 10:  # YYYY-MM-DD формат
                period_month = f"{period_month}T00:00:00"
            elif len(period_month) == 16:  # YYYY-MM-DDTHH:MM формат
                period_month = f"{period_month}:00"
            
            # Фильтруем по точному совпадению даты и времени
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
    
    @action(detail=False, methods=['get'])
    def periods(self, request):
        """Получить список всех уникальных периодов из базы данных"""
        # Получаем все уникальные периоды из переменных затрат
        periods = TruckVariableCosts.objects.values_list('period_month', flat=True).distinct().order_by('-period_month')
        
        # Форматируем периоды для отображения
        formatted_periods = []
        for period in periods:
            formatted_periods.append({
                'value': period.isoformat(),
                'label': period.strftime('%d %B %Y г.'),
                'date': period.date().isoformat(),
                'datetime': period.isoformat()
            })
        
        return Response(formatted_periods)