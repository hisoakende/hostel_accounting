from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.api import extend_docs
from accounts.api.serializers import UserSerializer
from accounts.models import User
from paginations import DefaultPagination
from permissions import IsThisUser
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
        return get_default_retrieve_response(request, self)

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
        return get_default_list_response_with_pagination(request, self)
