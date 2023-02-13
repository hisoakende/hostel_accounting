from typing import Any

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods_accounting.api import extend_docs
from goods_accounting.models import ProductCategory, Product, Purchase
from goods_accounting.utils import process_deletion_or_addition_product_purchase_request, \
    delete_product_from_purchase, add_product_to_purchase
from hostel_accounting.paginations import DefaultPagination
from hostel_accounting.permissions import ReadOnly, PurchasePermission, IsOwner
from hostel_accounting.serializers import ProductCategorySerializer, ProductSerializer, PurchaseSerializer
from hostel_accounting.utils import get_default_retrieve_response, get_all_fields_from_request, \
    get_default_list_response_with_pagination


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminUser | ReadOnly,)

    @extend_schema(**extend_docs.product_category_create)
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(**extend_docs.product_category_retrieve)
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return get_default_retrieve_response(request, self, ('fields', 'category_fields'))

    @extend_schema(**extend_docs.product_category_update)
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> None:
        raise MethodNotAllowed('patch')

    @extend_schema(**extend_docs.product_category_destroy)
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(**extend_docs.product_category_list)
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        fields_params = get_all_fields_from_request(request)
        serializer = self.serializer_class(self.queryset, many=True, **fields_params)
        return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = DefaultPagination

    @extend_schema(**extend_docs.product_create)
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(**extend_docs.product_retrieve)
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return get_default_retrieve_response(request, self, ('fields', 'category_fields'))

    @extend_schema(**extend_docs.product_update)
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(**extend_docs.product_partial_update)
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(**extend_docs.product_destroy)
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(**extend_docs.product_list)
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return get_default_list_response_with_pagination(request, self, ('fields', 'category_fields'))


class PurchaseViewSet(ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = (PurchasePermission,)
    pagination_class = DefaultPagination

    def perform_create(self, serializer: PurchaseSerializer) -> None:
        serializer.save(user=self.request.user)

    def get_queryset(self) -> QuerySet[Purchase]:
        if self.request.user.is_staff:
            return Purchase.objects.all().prefetch_related()
        return Purchase.objects.filter(user__rommates_group=self.request.user.roommates_group).prefetch_related()

    @extend_schema(**extend_docs.purchase_create)
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(**extend_docs.purchase_retrieve)
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return get_default_retrieve_response(request, self, (
            'fields', 'user_fields', 'product_fields', 'product_category_fields'))

    @extend_schema(exclude=True)
    def update(self, request: Request, *args: Any, **kwargs: Any) -> None:
        raise MethodNotAllowed('put')

    @extend_schema(exclude=True)
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> None:
        raise MethodNotAllowed('patch')

    @extend_schema(**extend_docs.purchase_destroy)
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(**extend_docs.purchase_list)
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        self.queryset = self.get_queryset()
        return get_default_list_response_with_pagination(request, self, (
            'fields', 'user_fields', 'product_fields', 'product_category_fields'))

    @extend_schema(**extend_docs.purchase_add_products)
    @action(detail=True, methods=['post'], permission_classes=(IsOwner | IsAdminUser,), url_path='add-products')
    def add_products(self, request: Request, pk: str) -> Response:
        purchase = self.get_object()
        return process_deletion_or_addition_product_purchase_request(request, purchase, add_product_to_purchase,
                                                                     status.HTTP_200_OK)

    @extend_schema(**extend_docs.purchase_delete_products)
    @action(detail=True, methods=['post'], permission_classes=(IsOwner | IsAdminUser,), url_path='delete-products')
    def delete_products(self, request: Request, pk: str) -> Response:
        purchase = self.get_object()
        return process_deletion_or_addition_product_purchase_request(request, purchase, delete_product_from_purchase,
                                                                     status.HTTP_204_NO_CONTENT)
