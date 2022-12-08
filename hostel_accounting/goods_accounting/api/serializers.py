from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from goods_accounting.models import ProductCategory, Product, Purchase, ProductPurchase
from utils import DynamicFieldsSerializerMixin, GetObjectByIdFromRequestSerializerMixin, \
    ChangeFieldsInDeepSerializersMixin


class ProductCategorySerializer(GetObjectByIdFromRequestSerializerMixin, DynamicFieldsSerializerMixin,
                                serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')


class ProductSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    category = ProductCategorySerializer(validate_by_id=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category')
        fields_serializer_data = (('category_fields', ('category',)),)


class ProductPurchaseSerializer(GetObjectByIdFromRequestSerializerMixin, DynamicFieldsSerializerMixin,
                                serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    name = serializers.ReadOnlyField(source='product.name')
    category = ProductCategorySerializer(source='product.category')

    class Meta:
        model = ProductPurchase
        fields = ('id', 'name', 'price', 'category')


class PurchaseSerializer(ChangeFieldsInDeepSerializersMixin, DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    user = UserSerializer()
    products = ProductPurchaseSerializer(source='productpurchase_set', many=True, validate_by_id=True)

    class Meta:
        model = Purchase
        fields = ('id', 'datetime', 'user', 'products')
        fields_serializer_data = (('user_fields', ('user',)),
                                  ('product_fields', ('products',)),
                                  ('product_category_fields', ('products', 'category')))
