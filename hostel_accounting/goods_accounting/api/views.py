from abc import ABC, abstractmethod
from typing import Type

from rest_framework.viewsets import ModelViewSet

from goods_accounting.api.mixins import RequiredFieldsMixin
from goods_accounting.api.permissions import IsStaffOrReadOnly
from goods_accounting.api.serializers import ProductCategorySerializer
from goods_accounting.models import ProductCategory, AbstractModel


class BaseView(ABC):

    @property
    @abstractmethod
    def model(self) -> Type[AbstractModel]:
        pass


class ProductCategoryViewSet(RequiredFieldsMixin, BaseView, ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (IsStaffOrReadOnly,)
    model = ProductCategory
