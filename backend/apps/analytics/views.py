from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date, datetime
from .models import ProfitabilityCalculation
from .serializers import (
    ProfitabilityCalculationSerializer,
    ProfitabilitySummarySerializer,
    TruckProfitabilitySerializer
)
from .services import AnalyticsService


class AnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProfitabilityCalculation.objects.all()
    serializer_class = ProfitabilityCalculationSerializer
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Получить сводку по прибыльности за период"""
        period_month = request.query_params.get('period_month')
        if not period_month:
            return Response(
                {'error': 'Необходимо указать period_month'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if len(period_month) == 7:  # YYYY-MM
                period_date = datetime.fromisoformat(f"{period_month}-01T00:00:00")
            elif len(period_month) == 10:  # YYYY-MM-DD
                period_date = datetime.fromisoformat(f"{period_month}T00:00:00")
            else:  # YYYY-MM-DDTHH:MM:SS
                period_date = datetime.fromisoformat(period_month)
        except ValueError:
            return Response(
                {'error': 'Неверный формат даты. Используйте YYYY-MM, YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        summary = AnalyticsService.get_profitability_summary(period_date)
        serializer = ProfitabilitySummarySerializer(summary)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trucks(self, request):
        """Получить прибыльность по тракам за период"""
        period_month = request.query_params.get('period_month')
        if not period_month:
            return Response(
                {'error': 'Необходимо указать period_month'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if len(period_month) == 7:  # YYYY-MM
                period_date = datetime.fromisoformat(f"{period_month}-01T00:00:00")
            elif len(period_month) == 10:  # YYYY-MM-DD
                period_date = datetime.fromisoformat(f"{period_month}T00:00:00")
            else:  # YYYY-MM-DDTHH:MM:SS
                period_date = datetime.fromisoformat(period_month)
        except ValueError:
            return Response(
                {'error': 'Неверный формат даты. Используйте YYYY-MM, YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        truck_data = AnalyticsService.get_truck_profitability(period_date)
        serializer = TruckProfitabilitySerializer(truck_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Получить тренды прибыльности за период"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'Необходимо указать start_date и end_date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if len(start_date) == 7:  # YYYY-MM
                start = datetime.fromisoformat(f"{start_date}-01T00:00:00")
            elif len(start_date) == 10:  # YYYY-MM-DD
                start = datetime.fromisoformat(f"{start_date}T00:00:00")
            else:  # YYYY-MM-DDTHH:MM:SS
                start = datetime.fromisoformat(start_date)
                
            if len(end_date) == 7:  # YYYY-MM
                end = datetime.fromisoformat(f"{end_date}-01T00:00:00")
            elif len(end_date) == 10:  # YYYY-MM-DD
                end = datetime.fromisoformat(f"{end_date}T00:00:00")
            else:  # YYYY-MM-DDTHH:MM:SS
                end = datetime.fromisoformat(end_date)
        except ValueError:
            return Response(
                {'error': 'Неверный формат даты. Используйте YYYY-MM, YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trends = AnalyticsService.get_profitability_trends(start, end)
        return Response(trends)
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Пересчитать прибыльность для периода"""
        period_month = request.data.get('period_month')
        if not period_month:
            return Response(
                {'error': 'Необходимо указать period_month'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if len(period_month) == 7:  # YYYY-MM
                period_date = datetime.fromisoformat(f"{period_month}-01T00:00:00")
            elif len(period_month) == 10:  # YYYY-MM-DD
                period_date = datetime.fromisoformat(f"{period_month}T00:00:00")
            else:  # YYYY-MM-DDTHH:MM:SS
                period_date = datetime.fromisoformat(period_month)
        except ValueError:
            return Response(
                {'error': 'Неверный формат даты. Используйте YYYY-MM, YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        calculations = AnalyticsService.calculate_profitability_for_period(period_date)
        serializer = ProfitabilityCalculationSerializer(calculations, many=True)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        """Получить список расчетов прибыльности"""
        queryset = self.get_queryset()
        
        # Фильтрация по месяцу
        period_month = request.query_params.get('period_month')
        if period_month:
            try:
                if len(period_month) == 7:  # YYYY-MM
                    period_date = datetime.fromisoformat(f"{period_month}-01T00:00:00")
                elif len(period_month) == 10:  # YYYY-MM-DD
                    period_date = datetime.fromisoformat(f"{period_month}T00:00:00")
                else:  # YYYY-MM-DDTHH:MM:SS
                    period_date = datetime.fromisoformat(period_month)
                queryset = queryset.filter(period_month=period_date)
            except ValueError:
                return Response(
                    {'error': 'Неверный формат даты. Используйте YYYY-MM, YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Фильтрация по траку
        truck_id = request.query_params.get('truck_id')
        if truck_id:
            queryset = queryset.filter(truck_id=truck_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)