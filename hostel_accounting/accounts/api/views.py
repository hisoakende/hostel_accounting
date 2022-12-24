from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.api import extend_docs
from accounts.api.serializers import UserSerializer, RoommatesGroupSerializer
from accounts.models import User, RoommatesGroup
from paginations import DefaultPagination
from permissions import IsThisUser, RoommatesGroupPermission
from utils import get_default_retrieve_response, get_default_list_response_with_pagination


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser | IsThisUser,)
    pagination_class = DefaultPagination

    @extend_schema(exclude=True)
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        raise MethodNotAllowed('post')

    @extend_schema(**extend_docs.user_retrieve)
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return get_default_retrieve_response(request, self, ('fields', 'roommates_group_fields'))

    @extend_schema(**extend_docs.user_update)
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(**extend_docs.user_partial_update)
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(**extend_docs.user_destroy)
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(**extend_docs.user_list)
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return get_default_list_response_with_pagination(request, self, ('fields', 'roommates_group_fields'))


class RoommatesGroupViewSet(ModelViewSet):
    queryset = RoommatesGroup.objects.all().select_related()
    serializer_class = RoommatesGroupSerializer
    permission_classes = (RoommatesGroupPermission,)
    pagination_class = DefaultPagination

    def perform_create(self, serializer: RoommatesGroupSerializer) -> None:
        super().perform_create(serializer)
        self.request.user.roommates_group = serializer.instance
        self.request.user.save()

    @extend_schema(**extend_docs.roommates_group_create)
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(**extend_docs.roommates_group_retrieve)
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return get_default_retrieve_response(request, self, ('fields', 'users_fields'))

    @extend_schema(**extend_docs.roommates_group_update)
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        raise MethodNotAllowed('patch')

    @extend_schema(**extend_docs.roommates_group_destroy)
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(**extend_docs.roommates_group_list)
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return get_default_list_response_with_pagination(request, self, ('fields', 'users_fields'))
