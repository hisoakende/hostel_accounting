from typing import OrderedDict

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from goods_accounting.models import ProductCategory, Product


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    category = PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'category')

    def to_representation(self, instance: Product) -> OrderedDict:
        response = super().to_representation(instance)
        category = ProductCategory.objects.get(pk=response['category'])
        response['category'] = ProductCategorySerializer(category).data
        return response
