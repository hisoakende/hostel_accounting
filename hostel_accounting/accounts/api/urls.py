from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, RoommatesGroupViewSet

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('roommates-groups', RoommatesGroupViewSet)

urlpatterns = [
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
