from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Truck
from .serializers import TruckSerializer, TruckCreateSerializer


class TruckViewSet(viewsets.ModelViewSet):
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