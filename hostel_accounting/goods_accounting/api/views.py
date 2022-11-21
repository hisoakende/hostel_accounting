from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods_accounting.api import extend_docs
from goods_accounting.api.paginations import ProductPagination
from goods_accounting.api.permissions import ReadOnly
from goods_accounting.api.serializers import ProductCategorySerializer, ProductSerializer
from goods_accounting.models import ProductCategory, Product
from utils import get_fields_from_request


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminUser | ReadOnly,)

    @extend_schema(**extend_docs.product_category_create)
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(**extend_docs.product_category_retrieve)
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        fields = get_fields_from_request(request)
        serializer = self.serializer_class(self.get_object(), fields=fields)
        return Response(serializer.data)

    @extend_schema(**extend_docs.product_category_update)
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().update(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        raise MethodNotAllowed

    @extend_schema(**extend_docs.product_category_destroy)
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().destroy(request, *args, **kwargs)

    @extend_schema(**extend_docs.product_category_list)
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        fields = get_fields_from_request(request)
        serializer = self.serializer_class(self.queryset, many=True, fields=fields)
        return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @extend_schema(**extend_docs.product_create)
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().create(request, *args, **kwargs)

    @extend_schema(**extend_docs.product_retrieve)
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        fields = get_fields_from_request(request)
        category_fields = get_fields_from_request(request, 'category_fields')
        serializer = self.serializer_class(self.get_object(), fields=fields, category_fields=category_fields)
        return Response(serializer.data)

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
        if not self.queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        fields = get_fields_from_request(request)
        category_fields = get_fields_from_request(request, 'category_fields')
        page = self.paginate_queryset(self.queryset)
        serializer = self.serializer_class(page, many=True, fields=fields, category_fields=category_fields)
        return self.get_paginated_response(serializer.data)
