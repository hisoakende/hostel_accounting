from rest_framework.routers import SimpleRouter

from .views import UserViewSet, RoommatesGroupViewSet

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('roommates-groups', RoommatesGroupViewSet)

urlpatterns = router.urls
