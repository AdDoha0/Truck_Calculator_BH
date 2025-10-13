"""
URL configuration for truck_calculate project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trucks/', include('apps.trucks.urls')),
    path('api/costs/', include('apps.costs.urls')),
    path('api/snapshots/', include('apps.snapshots.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)