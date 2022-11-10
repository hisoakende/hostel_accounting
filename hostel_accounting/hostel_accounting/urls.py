from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/goods-accounting/', include('goods_accounting.api.urls'))
]
