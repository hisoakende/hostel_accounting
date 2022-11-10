from rest_framework.routers import SimpleRouter

from .views import ProductCategoryViewSet

router = SimpleRouter()
router.register('product-category', ProductCategoryViewSet)

urlpatterns = router.urls
