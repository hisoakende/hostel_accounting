import unittest

from django.test import RequestFactory

from utils import *


class DynamicFieldsMixinModelSerializerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.serializer_class = type('SomeSerializer', (DynamicFieldsMixinModelSerializer,),
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
