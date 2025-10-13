from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date
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
        """Создать снимок текущего состояния с сегодняшней датой"""
        period_date = request.data.get('period_date', timezone.now().date())
        label = request.data.get('label', f'Снимок от {timezone.now().strftime("%d.%m.%Y %H:%M")}')
        
        snapshot = SnapshotService.create_snapshot(period_date, label)
        return Response(
            CostSnapshotSerializer(snapshot).data,
            status=status.HTTP_201_CREATED
        )