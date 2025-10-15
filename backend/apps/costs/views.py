from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import FixedCostsCommon, FixedCostsTruck, TruckVariableCosts, TruckCurrentVariableCosts
from .serializers import (
    FixedCostsCommonSerializer, 
    FixedCostsTruckSerializer, 
    TruckVariableCostsSerializer,
    TruckVariableCostsCreateSerializer,
    TruckCurrentVariableCostsSerializer,
    TruckCurrentVariableCostsCreateSerializer
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
        
        # Фильтрация по снимку (игнорируем 'current')
        snapshot_id = request.query_params.get('snapshot_id')
        if snapshot_id and snapshot_id != 'current':
            queryset = queryset.filter(snapshot_id=snapshot_id)
        
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
        """Получить список периодов на основе снимков"""
        from apps.snapshots.models import CostSnapshot
        snapshots = CostSnapshot.objects.all().order_by('-period_date', '-snapshot_at')
        formatted = [{
            'value': 'current',
            'label': 'Текущие данные',
            'date': 'current',
            'datetime': 'current'
        }]
        for s in snapshots:
            formatted.append({
                'value': str(s.id),
                'label': s.period_date.strftime('%d %B %Y г.'),
                'date': s.period_date.isoformat(),
                'datetime': s.snapshot_at.isoformat(),
            })
        return Response(formatted)
    
    @action(detail=False, methods=['get'])
    def by_period_with_snapshot(self, request):
        """Получить данные по snapshot: current или snapshot_id"""
        snapshot_id = request.query_params.get('snapshot_id') or request.query_params.get('period_month')
        if not snapshot_id:
            return Response({'error': 'snapshot_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Если запрошены текущие данные, возвращаем актуальные фиксированные затраты
        if snapshot_id == 'current':
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
        
        # Получаем снимок и связанные данные
        from apps.snapshots.models import CostSnapshot
        try:
            snapshot = CostSnapshot.objects.get(id=snapshot_id)
        except CostSnapshot.DoesNotExist:
            return Response({'error': 'snapshot not found'}, status=status.HTTP_404_NOT_FOUND)
        variable_costs = TruckVariableCosts.objects.filter(snapshot=snapshot)
        
        # Получаем фиксированные затраты из снимка
        fixed_costs_data = None
        from apps.snapshots.services import SnapshotService
        fixed_costs_data = SnapshotService.get_snapshot_details(snapshot)
        
        # Получаем общие фиксированные затраты из снимка
        common_costs_data = None
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


class TruckCurrentVariableCostsViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с текущими переменными затратами"""
    queryset = TruckCurrentVariableCosts.objects.all()
    serializer_class = TruckCurrentVariableCostsSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TruckCurrentVariableCostsCreateSerializer
        return TruckCurrentVariableCostsSerializer
    
    def list(self, request, *args, **kwargs):
        """Получить текущие переменные затраты"""
        queryset = self.get_queryset()
        
        # Фильтрация по траку
        truck_id = request.query_params.get('truck_id')
        if truck_id:
            queryset = queryset.filter(truck_id=truck_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Создать или обновить текущие переменные затраты для трака"""
        truck_id = request.data.get('truck')
        if not truck_id:
            return Response(
                {'error': 'truck field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем, есть ли уже запись для этого трака
        try:
            existing_record = TruckCurrentVariableCosts.objects.get(truck_id=truck_id)
            # Обновляем существующую запись
            serializer = self.get_serializer(existing_record, data=request.data)
        except TruckCurrentVariableCosts.DoesNotExist:
            # Создаем новую запись
            serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='by-truck/(?P<truck_id>[^/.]+)')
    def by_truck(self, request, truck_id=None):
        """Получить текущие переменные затраты для конкретного трака"""
        try:
            current_costs = TruckCurrentVariableCosts.objects.get(truck_id=truck_id)
            serializer = self.get_serializer(current_costs)
            return Response(serializer.data)
        except TruckCurrentVariableCosts.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def current_data(self, request):
        """Получить все текущие данные (фиксированные + переменные)"""
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
        
        # Получаем текущие переменные затраты
        current_variable_costs = TruckCurrentVariableCosts.objects.all()
        variable_costs_data = TruckCurrentVariableCostsSerializer(current_variable_costs, many=True).data
        
        return Response({
            'fixed_costs': {
                'common': common_costs_data,
                'trucks': trucks_data
            },
            'variable_costs': variable_costs_data,
            'common_costs': common_costs_data,
            'snapshot': None  # Нет снимка для текущих данных
        })