from typing import Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.api.serializers import UserSerializer
from goods_accounting.models import ProductCategory, Product, Purchase, ProductPurchase
from utils import DynamicFieldsSerializerMixin, GetObjectByIdFromRequestSerializerMixin, \
    ChangeFieldsInDeepSerializersMixin


class ProductCategorySerializer(GetObjectByIdFromRequestSerializerMixin, DynamicFieldsSerializerMixin,
                                serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')


class ProductSerializer(ChangeFieldsInDeepSerializersMixin, DynamicFieldsSerializerMixin,
                        serializers.ModelSerializer):
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

    @staticmethod
    def val(data: Any) -> None:
        if type(data) is not dict:
            raise ValidationError('Значения должны быть dict')
        if not data.get('product', False) or not data.get('price', False):
            raise ValidationError('Должны быть поля \'product\' и \'price\'')
        if any(type(element) != int for element in data.values()):
            raise ValidationError('Поля должны быть integer')
        if data['price'] < 0:
            raise ValidationError(f'Цена не может быть отрицательной ({data["price"]})')

    @staticmethod
    def get_obj(data: dict[str, int]) -> tuple[Product, int]:
        obj = Product.objects.filter(pk=data['product'])
        if not obj.exists():
            raise ValidationError(f'Объект c id \'{data["product"]}\' не существует')
        return obj[0], data['price']

    def to_representation(self, instance: ProductPurchase) -> Any:
        if instance.product is None:
            return {field: instance.price if field == 'price' else None for field in self.fields}
        return super().to_representation(instance)


class PurchaseSerializer(ChangeFieldsInDeepSerializersMixin, DynamicFieldsSerializerMixin,
                         serializers.ModelSerializer):
    user = UserSerializer(required=False, validate_by_id=True)
    products = ProductPurchaseSerializer(source='productpurchase_set', many=True, validate_by_id=True)

    class Meta:
        model = Purchase
        fields = ('id', 'datetime', 'user', 'products')
        fields_serializer_data = (('user_fields', ('user',)),
                                  ('product_fields', ('products',)),
                                  ('product_category_fields', ('products', 'category')))

    @staticmethod
    def create(validated_data: dict[str, Any]) -> Purchase:
        purchase = Purchase.objects.create(user=validated_data['user'])
        for product, price in validated_data['productpurchase_set']:
            ProductPurchase.objects.create(purchase=purchase, product=product, price=price)
        return purchase
