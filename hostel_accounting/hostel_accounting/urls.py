from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/goods-accounting/', include('goods_accounting.api.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularRedocView.as_view(), name='docs')
]
