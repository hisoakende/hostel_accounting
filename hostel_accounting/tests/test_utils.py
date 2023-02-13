import unittest

import django.test
from django.test import RequestFactory
from rest_framework.fields import IntegerField

from accounts.models import User
from hostel_accounting.serializers import PurchaseSerializer, ProductPurchaseSerializer
from goods_accounting.models import ProductCategory, Product, Purchase
from hostel_accounting.utils import *


class DynamicFieldsMixinTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.serializer_class = type('SomeSerializer', (DynamicFieldsSerializerMixin,),
                                    {'fields': {'field1': '', 'field2': '', 'field3': ''}})

    def test_fields_is_none(self) -> None:
        serializer = self.serializer_class()
        result = tuple(serializer.fields.keys())
        self.assertEqual(result, ('field1', 'field2', 'field3'))

    def test_fields_is_not_none(self) -> None:
        serializer = self.serializer_class(fields=('field1', 'field2', 'extra_field'))
        result = tuple(serializer.fields.keys())
        self.assertEqual(result, ('field1', 'field2'))


class GetAllFieldsFromRequestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.factory = RequestFactory()

    def test_non_query_params(self):
        request = self.factory.get('/')
        request.query_params = {}
        result = get_all_fields_from_request(request)
        self.assertEqual(result, {'fields': None})

    def test_non_fields(self):
        request = self.factory.get('/?fields=&category_fields=')
        request.query_params = {'fields': request.GET.get('fields'),
                                'category_fields': request.GET.get('category_fields')}
        result = get_all_fields_from_request(request, ('fields', 'category_fields'))
        self.assertEqual(result, {'fields': [''], 'category_fields': ['']})

    def test_get_fields(self):
        request = self.factory.get('/?fields=id,name&category_fields=name')
        request.query_params = {'fields': request.GET.get('fields'),
                                'category_fields': request.GET.get('category_fields')}
        result = get_all_fields_from_request(request, ('fields', 'category_fields'))
        expected_result = {'fields': ['id', 'name'], 'category_fields': ['name']}
        self.assertEqual(result, expected_result)


class GetObjectByIdFromRequestSerializerMixinTest(django.test.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        ProductCategory.objects.create(name="Some category")
        meta = type("Meta", (), {"model": ProductCategory})
        cls.default_to_internal_value_value = None
        serializer_ = type("SomeSerializer", (),
                           {"to_internal_value": lambda self, data: cls.default_to_internal_value_value, "Meta": meta})
        cls.some_class = type("SomeClass", (GetObjectByIdFromRequestSerializerMixin, serializer_,), {})
        cls.some_obj = cls.some_class()  # без атрибута 'validate_by_id' - обработка происходит по умолчанию

    def test_validate_type_raises_exception(self) -> None:
        self.assertRaises(ValidationError, self.some_obj.val, "test string")

    def test_validate_type_returns_none(self) -> None:
        self.assertIsNone(self.some_obj.val(123))

    def test_get_obj_raises_exception(self) -> None:
        self.assertRaises(ValidationError, self.some_obj.get_obj, 2)

    def test_get_obj_returns_obj(self) -> None:
        self.assertEqual(1, self.some_obj.get_obj(1).pk)

    def test_to_internal_value_return_default_value(self) -> None:
        self.assertEqual(self.default_to_internal_value_value, self.some_obj.to_internal_value("test string"))

    def test_to_internal_value_return_obj(self) -> None:
        some_class_with_processing_by_id = self.some_class(validate_by_id=True)
        self.assertEqual(1, some_class_with_processing_by_id.to_internal_value(1).pk)


class GetFieldHandlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        user = User.objects.create(username="admin", email="admin@mail.com")
        category = ProductCategory.objects.create(name="category")
        product = Product.objects.create(name="product", category=category)
        purchase = Purchase.objects.create(user=user)
        purchase.productpurchase_set.create(product=product, price=1000)
        cls.serializer = PurchaseSerializer(purchase)

    def test_field_name_is_none(self) -> None:
        self.assertIsNone(get_field_handler("non-existent field", self.serializer))

    def test_field_name_is_list_serializer(self) -> None:
        self.assertEqual(ProductPurchaseSerializer, get_field_handler("products", self.serializer).__class__)

    def test_field_name_is_field_or_one_object_serializer(self) -> None:
        self.assertEqual(IntegerField, get_field_handler("id", self.serializer).__class__)
