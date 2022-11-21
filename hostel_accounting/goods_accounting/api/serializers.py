from typing import OrderedDict, Any

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from goods_accounting.models import ProductCategory, Product
from utils import DynamicFieldsModelSerializer


class ProductCategorySerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')


class ProductSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    category = PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'category')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.category_fields = kwargs.pop('category_fields', None)
        super().__init__(*args, **kwargs)

    def to_representation(self, instance: Product) -> OrderedDict:
        response = super().to_representation(instance)
        if response.get('category') is not None:
            category = ProductCategory.objects.get(pk=response['category'])
            response['category'] = ProductCategorySerializer(category, fields=self.category_fields).data
        return response
