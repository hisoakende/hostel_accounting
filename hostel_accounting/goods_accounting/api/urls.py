from rest_framework.routers import SimpleRouter

from .views import ProductCategoryViewSet, ProductViewSet, PurchaseViewSet

router = SimpleRouter()
router.register('product-categories', ProductCategoryViewSet)
router.register('products', ProductViewSet)
router.register('purchases', PurchaseViewSet, basename='purchase')

urlpatterns = router.urls
