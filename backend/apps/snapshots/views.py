from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date, datetime
from .models import CostSnapshot
from .serializers import (
    CostSnapshotSerializer, 
    SnapshotComparisonSerializer,
    CreateSnapshotSerializer
)
from .services import SnapshotService


class CostSnapshotViewSet(viewsets.ModelViewSet):
    queryset = CostSnapshot.objects.all()
    serializer_class = CostSnapshotSerializer
    
    def list(self, request, *args, **kwargs):
        """Получить список всех снимков"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Создать новый снимок текущего состояния"""
        serializer = CreateSnapshotSerializer(data=request.data)
        if serializer.is_valid():
            period_date = serializer.validated_data['period_date']
            label = serializer.validated_data.get('label', '')
            
            snapshot = SnapshotService.create_snapshot(period_date, label)
            return Response(
                CostSnapshotSerializer(snapshot).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        """Получить конкретный снимок"""
        snapshot = get_object_or_404(CostSnapshot, pk=pk)
        serializer = self.get_serializer(snapshot)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        """Удалить снимок"""
        snapshot = get_object_or_404(CostSnapshot, pk=pk)
        snapshot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])
    def compare(self, request):
        """Сравнить несколько снимков"""
        snapshot_ids = request.data.get('snapshot_ids', [])
        if not snapshot_ids or len(snapshot_ids) < 2:
            return Response(
                {'error': 'Необходимо указать минимум 2 снимка для сравнения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comparison_data = SnapshotService.get_snapshot_comparison(snapshot_ids)
        return Response(comparison_data)
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Восстановить текущие стоимости из снимка"""
        success = SnapshotService.restore_from_snapshot(pk)
        if success:
            return Response({'message': 'Стоимости успешно восстановлены из снимка'})
        return Response(
            {'error': 'Ошибка при восстановлении снимка'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'])
    def create_current(self, request):
        """Создать снимок текущего состояния с текущей датой и временем"""
        period_date = request.data.get('period_date', timezone.now())
        label = request.data.get('label', f'Снимок от {timezone.now().strftime("%d.%m.%Y %H:%M:%S")}')
        
        snapshot = SnapshotService.create_snapshot(period_date, label)
        return Response(
            CostSnapshotSerializer(snapshot).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'])
    def create_from_current_data(self, request):
        """Создать снимок из текущих данных (включая переменные затраты)"""
        period_date = request.data.get('period_date', timezone.now())
        label = request.data.get('label', f'Снимок от {timezone.now().strftime("%d.%m.%Y %H:%M:%S")}')
        
        # Преобразуем period_date в datetime если нужно
        if isinstance(period_date, str):
            try:
                if len(period_date) == 7:  # YYYY-MM
                    period_date = datetime.fromisoformat(f"{period_date}-01T00:00:00")
                elif len(period_date) == 10:  # YYYY-MM-DD
                    period_date = datetime.fromisoformat(f"{period_date}T00:00:00")
                else:
                    period_date = datetime.fromisoformat(period_date)
            except ValueError:
                return Response(
                    {'error': 'Неверный формат даты'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        # приведение к дате для модели
        if isinstance(period_date, datetime):
            period_date = period_date.date()
        
        snapshot = SnapshotService.create_snapshot_from_current_data(period_date, label)
        return Response(
            CostSnapshotSerializer(snapshot).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'])
    def by_period(self, request):
        """Найти последний снимок с period_date <= указанного периода.

        query param: period_month = YYYY-MM | YYYY-MM-DD | YYYY-MM-DDTHH:MM:SS
        """
        period_month = request.query_params.get('period_month')
        if not period_month:
            return Response({'error': 'Необходимо указать period_month'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Принимаем YYYY-MM, YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS
            if len(period_month) == 7:
                period_date = datetime.fromisoformat(f"{period_month}-01T00:00:00")
            elif len(period_month) == 10:
                period_date = datetime.fromisoformat(f"{period_month}T00:00:00")
            else:
                period_date = datetime.fromisoformat(period_month)
        except ValueError:
            return Response({'error': 'Неверный формат даты. Используйте YYYY-MM, YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS'}, status=status.HTTP_400_BAD_REQUEST)

        snapshot = SnapshotService.get_latest_snapshot_for_period(period_date)
        if not snapshot:
            return Response({'detail': 'Снимок не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CostSnapshotSerializer(snapshot).data)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Детали снимка: общие фикс-стоимости и по тракам (опционально по одному траку).

        query param: truck_id (optional)
        """
        snapshot = get_object_or_404(CostSnapshot, pk=pk)

        truck_id = request.query_params.get('truck_id')
        common = SnapshotService.get_common_costs_from_snapshot(snapshot)

        from .models import CostSnapshotTruck
        truck_costs_qs = CostSnapshotTruck.objects.filter(snapshot=snapshot)
        if truck_id:
            truck_costs_qs = truck_costs_qs.filter(truck_id=truck_id)

        data = {
            'snapshot': CostSnapshotSerializer(snapshot).data,
            'common': common,
            'trucks': [
                {
                    'truck_id': t.truck.id,
                    'truck_tractor_no': t.truck.tractor_no,
                    'truck_payment': t.truck_payment,
                    'trailer_payment': t.trailer_payment,
                    'physical_damage_insurance_truck': t.physical_damage_insurance_truck,
                    'physical_damage_insurance_trailer': t.physical_damage_insurance_trailer,
                }
                for t in truck_costs_qs
            ]
        }
        return Response(data)