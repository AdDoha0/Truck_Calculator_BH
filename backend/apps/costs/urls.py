from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FixedCostsCommonViewSet, FixedCostsTruckViewSet, TruckVariableCostsViewSet

router = DefaultRouter()
router.register(r'common', FixedCostsCommonViewSet, basename='fixed-costs-common')
router.register(r'truck', FixedCostsTruckViewSet, basename='fixed-costs-truck')
router.register(r'variable', TruckVariableCostsViewSet, basename='variable-costs')

urlpatterns = [
    path('', include(router.urls)),
]

