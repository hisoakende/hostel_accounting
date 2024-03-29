from copy import copy, deepcopy

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiExample, inline_serializer
from rest_framework import serializers

from hostel_accounting import extend_docs_global

"""ProductCategoryViewSet"""

product_category_fields = copy(extend_docs_global.fields_query_parameter)
product_category_fields.examples = [
    OpenApiExample(
        'Возвращаются поля \'id\', \'name\'',
        value='id,name'
    )
]

product_category_create = {
    'summary': 'Создать категорию',
    'description': 'Доступно только для администраторов'
}

product_category_retrieve = {
    'summary': 'Получить категорию',
    'description': 'Доступно для всех',
    'parameters': [
        product_category_fields,
        extend_docs_global.id_path_parameter
    ]
}

product_category_update = {
    'summary': 'Обновить категорию',
    'description': 'Доступно только для администраторов',
    'parameters': [
        extend_docs_global.id_path_parameter
    ]
}

product_category_destroy = {
    'summary': 'Удалить категорию',
    'description': 'Доступно только для администраторов',
    'parameters': [
        extend_docs_global.id_path_parameter
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

product_fields = copy(extend_docs_global.fields_query_parameter)
product_fields.examples = [
    OpenApiExample(
        'Возвращаются поля \'id\', \'name\'',
        value='id,name'
    )
]

product_category_fields = OpenApiParameter(
    'category_fields',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Позволяет указать у связанной модели \'product_category\' только те поля, которые следует вернуть',
    examples=[
        OpenApiExample(
            'Возвращаются поля \'id\', \'name\'',
            value='id,name'
        )
    ]
)

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
        product_category_fields,
        extend_docs_global.id_path_parameter
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
        extend_docs_global.id_path_parameter
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
        extend_docs_global.id_path_parameter
    ],
    'responses': {
        200: product_response_schema
    },
    'examples': [
        product_get_response
    ]
}

product_destroy = {
    'summary': 'Удалить продукт',
    'description': 'Доступно для всех',
    'parameters': [
        extend_docs_global.id_path_parameter
    ]
}

product_list = {
    'summary': 'Получить продукты',
    'description': 'Доступно для всех',
    'parameters': [
        product_fields,
        product_category_fields,
        extend_docs_global.page_param_ru,
        extend_docs_global.page_size_param_ru
    ],
    'responses': {
        200: product_response_schema
    },
    'examples': [
        product_get_response
    ]
}

"""PurchaseViewSet"""

purchase_fields = deepcopy(extend_docs_global.fields_query_parameter)
purchase_fields.examples = [
    OpenApiExample(
        'Возвращаются поля \'id\', \'user\'',
        value='id,user'
    )
]

purchase_user_fields = OpenApiParameter(
    'user_fields',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Позволяет указать у связанной модели \'user\' только те поля, которые следует вернуть',
    examples=[
        OpenApiExample(
            'Возвращаются поля \'username\', \'email\'',
            value='username,email'
        )
    ]
)

purchase_product_fields = OpenApiParameter(
    'product_fields',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Позволяет указать у связанной модели \'product\' только те поля, которые следует вернуть',
    examples=[
        OpenApiExample(
            'Возвращаются поля \'id\', \'name\'',
            value='id,name'
        )
    ]
)

purchase_product_category_fields = OpenApiParameter(
    'product_category_fields',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Позволяет указать у связанной модели \'product\' у поля-модели \'category\' '
                'только те поля, которые следует вернуть',
    examples=[
        OpenApiExample(
            'Возвращаются поля \'id\', \'name\'',
            value='id,name'
        )
    ]
)

create_purchase_request_schema = inline_serializer(
    name='purchase',
    fields={
        'products': serializers.ListField(child=inline_serializer(
            name='products',
            fields={
                "product": serializers.IntegerField(),
                "price": serializers.IntegerField()
            }
        ))
    }
)

add_or_delete_product_purchase_schema = serializers.ListSerializer(child=inline_serializer(
    name='products_purchase',
    fields={
        "product": serializers.IntegerField(),
        "price": serializers.IntegerField()
    }
))

purchase_create = {
    'summary': 'Создать покупку',
    'description': 'Доступно для авторизированных пользователей',
    'request': create_purchase_request_schema
}

purchase_retrieve = {
    'summary': 'Получить покупку',
    'description': 'Доступно для группы пользователя, совершившего покупку, или для администратора',
    'parameters': [
        purchase_fields,
        purchase_user_fields,
        purchase_product_fields,
        purchase_product_category_fields,
        extend_docs_global.id_path_parameter
    ]
}

purchase_destroy = {
    'summary': 'Удалить покупку',
    'description': 'Доступно для пользователя, совершившего эту покупку, или для администратора',
    'parameters': [
        extend_docs_global.id_path_parameter
    ]
}

purchase_list = {
    'summary': 'Получить покупки',
    'description': 'Доступно для авторизированных пользователй. Если запрос делает администратор,'
                   'то возвращаются все покупки, если нет, то только покупки пользователя, '
                   'сделавшего запрос, и его сожителей (при наличии)',
    'parameters': [
        purchase_fields,
        purchase_user_fields,
        purchase_product_fields,
        purchase_product_category_fields,
        extend_docs_global.page_param_ru,
        extend_docs_global.page_size_param_ru
    ]
}

purchase_add_products = {
    'summary': 'Добавить продукты в покупку',
    'description': 'Доступно для пользователя, совершившего эту покупку, или для администратора',
    'request': add_or_delete_product_purchase_schema,
    'parameters': [
        extend_docs_global.id_path_parameter
    ]
}

purchase_delete_products = {
    'summary': 'Удалить продукты из покупки',
    'description': 'Доступно для пользователя, совершившего эту покупку, или для администратора',
    'request': add_or_delete_product_purchase_schema,
    'responses': {
        204: None
    },
    'parameters': [
        extend_docs_global.id_path_parameter
    ]
}
