from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.api import extend_docs
from accounts.models import User, RoommatesGroup
from accounts.utils import get_response_while_processing_groups_purchases
from hostel_accounting.paginations import DefaultPagination
from hostel_accounting.permissions import IsThisUser, RoommatesGroupPermission, IsAuthenticatedAndWithGroup
from hostel_accounting.serializers import UserSerializer, RoommatesGroupSerializer
from hostel_accounting.utils import get_default_retrieve_response, get_default_list_response_with_pagination


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

    @extend_schema(**extend_docs.roommates_group_purchases)
    @action(detail=False, methods=['GET'], permission_classes=(IsAuthenticatedAndWithGroup,), url_path='purchases')
    def get_purchases_from_users_group(self, request: Request) -> Response:
        """Возвращает все покупки группы, если таковая имеется, в которой состоит пользователь, выполнивший запрос"""

        self.kwargs['pk'] = request.user.roommates_group.pk
        roommates_group = self.get_object()
        return get_response_while_processing_groups_purchases(request, roommates_group)
