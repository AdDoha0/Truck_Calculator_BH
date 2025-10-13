from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CostSnapshotViewSet

router = DefaultRouter()
router.register(r'', CostSnapshotViewSet, basename='snapshots')

urlpatterns = [
    path('', include(router.urls)),
]

