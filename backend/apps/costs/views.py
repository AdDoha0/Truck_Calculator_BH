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
            period_month = serializer.validated_data['period_month']
            
            # Проверяем, есть ли уже снимок для этого периода
            existing_variable_costs = TruckVariableCosts.objects.filter(
                period_month=period_month
            ).first()
            
            if existing_variable_costs and existing_variable_costs.cost_snapshot:
                # Используем существующий снимок
                snapshot = existing_variable_costs.cost_snapshot
            else:
                # Создаем новый снимок текущих фиксированных затрат
                from apps.snapshots.services import SnapshotService
                snapshot = SnapshotService.create_snapshot(
                    period_month, 
                    f"Автоматический снимок для {period_month.strftime('%Y-%m-%d')}"
                )
            
            # Создаем переменные затраты со ссылкой на снимок
            serializer.save(cost_snapshot=snapshot)
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
        
        # Добавляем опцию "Текущие данные" в начало списка
        formatted_periods.append({
            'value': 'current',
            'label': 'Текущие данные',
            'date': 'current',
            'datetime': 'current'
        })
        
        for period in periods:
            formatted_periods.append({
                'value': period.isoformat(),
                'label': period.strftime('%d %B %Y г.'),
                'date': period.date().isoformat(),
                'datetime': period.isoformat()
            })
        
        return Response(formatted_periods)
    
    @action(detail=False, methods=['get'])
    def by_period_with_snapshot(self, request):
        """Получить переменные затраты за период с фиксированными затратами из снимка"""
        period_month = request.query_params.get('period_month')
        if not period_month:
            return Response({'error': 'period_month required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Если запрошены текущие данные, возвращаем актуальные фиксированные затраты
        if period_month == 'current':
            from apps.costs.models import FixedCostsCommon, FixedCostsTruck
            from apps.trucks.models import Truck
            
            # Получаем текущие общие фиксированные затраты
            try:
                common_costs = FixedCostsCommon.objects.first()
                common_costs_data = {
                    'ifta': common_costs.ifta if common_costs else 0,
                    'insurance': common_costs.insurance if common_costs else 0,
                    'eld': common_costs.eld if common_costs else 0,
                    'tablet': common_costs.tablet if common_costs else 0,
                    'tolls': common_costs.tolls if common_costs else 0,
                }
            except:
                common_costs_data = {
                    'ifta': 0, 'insurance': 0, 'eld': 0, 'tablet': 0, 'tolls': 0
                }
            
            # Получаем текущие фиксированные затраты по тракам
            trucks_data = []
            trucks = Truck.objects.all()
            for truck in trucks:
                try:
                    truck_costs = FixedCostsTruck.objects.get(truck=truck)
                    trucks_data.append({
                        'truck_id': truck.id,
                        'truck_tractor_no': truck.tractor_no,
                        'truck_payment': truck_costs.truck_payment,
                        'trailer_payment': truck_costs.trailer_payment,
                        'physical_damage_insurance_truck': truck_costs.physical_damage_insurance_truck,
                        'physical_damage_insurance_trailer': truck_costs.physical_damage_insurance_trailer,
                    })
                except FixedCostsTruck.DoesNotExist:
                    trucks_data.append({
                        'truck_id': truck.id,
                        'truck_tractor_no': truck.tractor_no,
                        'truck_payment': 0,
                        'trailer_payment': 0,
                        'physical_damage_insurance_truck': 0,
                        'physical_damage_insurance_trailer': 0,
                    })
            
            return Response({
                'variable_costs': [],  # Для текущих данных переменных затрат нет
                'fixed_costs': {
                    'common': common_costs_data,
                    'trucks': trucks_data
                },
                'common_costs': common_costs_data,
                'snapshot': None  # Нет снимка для текущих данных
            })
        
        # Обрабатываем различные форматы дат
        if len(period_month) == 7:  # YYYY-MM формат
            period_month = f"{period_month}-01T00:00:00"
        elif len(period_month) == 10:  # YYYY-MM-DD формат
            period_month = f"{period_month}T00:00:00"
        elif len(period_month) == 16:  # YYYY-MM-DDTHH:MM формат
            period_month = f"{period_month}:00"
        
        # Получаем переменные затраты за период
        variable_costs = TruckVariableCosts.objects.filter(period_month=period_month)
        
        # Получаем снимок из первой записи (все записи за период должны иметь один снимок)
        snapshot = None
        if variable_costs.exists():
            snapshot = variable_costs.first().cost_snapshot
        
        # Получаем фиксированные затраты из снимка
        fixed_costs_data = None
        if snapshot:
            from apps.snapshots.services import SnapshotService
            fixed_costs_data = SnapshotService.get_snapshot_details(snapshot)
        
        # Получаем общие фиксированные затраты из снимка
        common_costs_data = None
        if snapshot:
            from apps.snapshots.models import CostSnapshotCommon
            try:
                snapshot_common = CostSnapshotCommon.objects.get(snapshot=snapshot)
                common_costs_data = {
                    'ifta': snapshot_common.ifta,
                    'insurance': snapshot_common.insurance,
                    'eld': snapshot_common.eld,
                    'tablet': snapshot_common.tablet,
                    'tolls': snapshot_common.tolls,
                }
            except CostSnapshotCommon.DoesNotExist:
                pass
        
        return Response({
            'variable_costs': TruckVariableCostsSerializer(variable_costs, many=True).data,
            'fixed_costs': fixed_costs_data,
            'common_costs': common_costs_data,
            'snapshot': {
                'id': snapshot.id,
                'period_date': snapshot.period_date.isoformat(),
                'snapshot_at': snapshot.snapshot_at.isoformat(),
                'label': snapshot.label
            } if snapshot else None
        })