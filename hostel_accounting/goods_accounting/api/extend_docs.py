from copy import copy

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiExample, inline_serializer
from rest_framework import serializers

id_path_parameter = OpenApiParameter(
    'id',
    type=OpenApiTypes.INT,
    location=OpenApiParameter.PATH
)

fields_query_parameter = OpenApiParameter(
    'fields',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Позволяет указать только те поля, которые следует вернуть',
)

"""ProductCategoryViewSet"""

product_category_fields = copy(fields_query_parameter)
product_category_fields.examples.append(OpenApiExample(
    'Возвращаются поля \'id\', \'name\'',
    value='id,name'
))

product_category_create = {
    'summary': 'Создать категорию',
    'description': 'Доступно только для администраторов'
}

product_category_retrieve = {
    'summary': 'Получить категорию',
    'description': 'Доступно для всех',
    'parameters': [
        product_category_fields,
        id_path_parameter
    ]
}

product_category_update = {
    'summary': 'Обновить категорию',
    'description': 'Доступно только для администраторов',
    'parameters': [
        id_path_parameter
    ]
}

product_category_destroy = {
    'summary': 'Удалить категорию',
    'description': 'Доступно только для администраторов',
    'parameters': [
        id_path_parameter
    ]
}

product_category_list = {
    'summary': 'Получить категории',
    'description': 'Доступно для всех',
    'parameters': [
        product_category_fields
    ]
}

"""ProductViewSet"""

product_fields = copy(fields_query_parameter)
product_fields.examples.append(OpenApiExample(
    'Возвращаются поля \'id\', \'name\'',
    value='id,name'
))

product_response_schema = inline_serializer(
    name='product',
    fields={
        'id': serializers.IntegerField(),
        'name': serializers.CharField(max_length=63),
        'category': inline_serializer(
            name='category',
            fields={
                'id': serializers.IntegerField(),
                'name': serializers.CharField(max_length=63)
            }
        )
    }
)

product_get_response = OpenApiExample(
    'Example',
    value={
        'id': 0,
        'name': 'string',
        'category': {
            'id': 0,
            'name': 'string'
        }
    },
    response_only=True
)

product_create = {
    'summary': 'Создать продукт',
    'description': 'Доступно для всех',
    'responses': {
        201: product_response_schema
    }
}

product_retrieve = {
    'summary': 'Получить продукт',
    'description': 'Доступно для всех',
    'parameters': [
        product_fields,
        id_path_parameter
    ],
    'responses': {
        200: product_response_schema
    },
    'examples': [product_get_response]
}

product_update = {
    'summary': 'Обновить продукт',
    'description': 'Доступно для всех',
    'parameters': [
        id_path_parameter
    ],
    'responses': {
        200: product_response_schema
    },
    'examples': [product_get_response]
}

product_partial_update = {
    'summary': 'Частично обновить продукт',
    'description': 'Доступно для всех',
    'parameters': [
        id_path_parameter
    ],
    'responses': {
        200: product_response_schema
    },
    'examples': [product_get_response]
}

product_destroy = {
    'summary': 'Удалить продукт',
    'description': 'Доступно для всех',
    'parameters': [
        id_path_parameter
    ]
}

product_list = {
    'summary': 'Получить продукты',
    'description': 'Доступно для всех',
    'responses': {
        200: product_response_schema
    },
    'examples': [product_get_response]
}
