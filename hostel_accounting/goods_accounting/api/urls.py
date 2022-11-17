from rest_framework.routers import SimpleRouter

from .views import ProductCategoryViewSet, ProductViewSet

router = SimpleRouter()
router.register('product-categories', ProductCategoryViewSet)
router.register('products', ProductViewSet)

urlpatterns = router.urls
