from copy import deepcopy

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

from goods_accounting.api.extend_docs import purchase_product_fields, purchase_product_category_fields
from hostel_accounting import extend_docs_global
from hostel_accounting.serializers import AllGroupsPurchasesSerializer

"""UserViewSet"""

user_fields = deepcopy(extend_docs_global.fields_query_parameter)
user_fields.examples = [
    OpenApiExample(
        'Возвращаются поля \'id\', \'username\'',
        value='id,username'
    )
]

user_roommates_group_fields = OpenApiParameter(
    'roommates_group_fields',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Позволяет указать у связанной модели \'roommates_group\' только те поля, которые следует вернуть',
    examples=[
        OpenApiExample(
            'Возвращаются поля \'id\', \'name\'',
            value='id,name'
        )
    ]
)

user_retrieve = {
    'summary': 'Получить пользователя',
    'description': 'Доступно для администраторов и для пользователя-владельца данных',
    'parameters': [
        user_fields,
        user_roommates_group_fields,
        extend_docs_global.id_path_parameter
    ]
}

user_update = {
    'summary': 'Обновить пользователя',
    'description': 'Доступно для администраторов и для пользователя-владельца данных',
    'parameters': [
        extend_docs_global.id_path_parameter
    ]
}

user_partial_update = {
    'summary': 'Частично обновить пользователя',
    'description': 'Доступно для администраторов и для пользователя-владельца данных',
    'parameters': [
        extend_docs_global.id_path_parameter
    ]
}

user_destroy = {
    'summary': 'Удалить пользователя',
    'description': 'Доступно для администраторов и для пользователя-владельца данных',
    'parameters': [
        extend_docs_global.id_path_parameter
    ]
}

user_list = {
    'summary': 'Получить пользователей',
    'description': 'Доступно только для администраторов',
    'parameters': [
        user_fields,
        user_roommates_group_fields,
        extend_docs_global.page_param_ru,
        extend_docs_global.page_size_param_ru
    ]
}

"""RoommatesGroupViewSet"""

roommates_group_fields = deepcopy(extend_docs_global.fields_query_parameter)
roommates_group_fields.examples = [
    OpenApiExample(
        'Возвращаются поля \'id\', \'created_at\'',
        value='id,created_at'
    )
]

roommates_group_users_fields = OpenApiParameter(
    'user_fields',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Позволяет указать у связанной модели \'user\' только те поля, которые следует вернуть',
    examples=[
        OpenApiExample(
            'Возвращаются поля \'id\', \'name\'',
            value='id,name'
        )
    ]
)

roommates_group_create = {
    'summary': 'Cоздать группу сожителей',
    'description': 'Доступно для авторизированных пользователей без группы'
}

roommates_group_retrieve = {
    'summary': 'Получить группу сожителей',
    'description': 'Доступно для авторизированных пользователей. Если запрос совершает администратор, '
                   'то ему разрешен доступ к любой группе. Если запрос совершает обычный пользователь, '
                   'то ему разрешен доступ только к своей группе',
    'parameters': [
        roommates_group_fields,
        roommates_group_users_fields,
        extend_docs_global.id_path_parameter
    ]
}

roommates_group_update = {
    'summary': 'Обновить группу сожителей',
    'description': 'Доступно для авторизированных пользователей. Если запрос совершает администратор, '
                   'то ему разрешен доступ к любой группе. Если запрос совершает обычный пользователь, '
                   'то ему разрешен доступ только к своей группе',
    'parameters': [
        extend_docs_global.id_path_parameter
    ]
}

roommates_group_list = {
    'summary': 'Получить группы сожителей',
    'description': 'Доступно только для администраторов',
    'parameters': [
        roommates_group_fields,
        roommates_group_users_fields,
        extend_docs_global.page_param_ru,
        extend_docs_global.page_size_param_ru
    ]
}

roommates_group_destroy = {
    'summary': 'Удалить группу сожителей',
    'description': 'Доступно только для администраторов',
    'parameters': [
        extend_docs_global.id_path_parameter
    ]
}

roommates_group_purchases_fields = deepcopy(extend_docs_global.fields_query_parameter)
roommates_group_purchases_fields.examples = [
    OpenApiExample(
        'Возвращаются поля \'roommates_group\', \'users_purchases\'',
        value='roommates_group,users_purchases'
    )
]
roommates_group_fields.name = 'roommates_group_fields'
roommates_group_fields.description = 'Позволяет указать у связанной модели \'roommates_group\' ' \
                                     'только те поля, которые следует вернуть'

roommates_group_purchases = {
    'summary': 'Получить все покупки комнаты пользователя',
    'description': 'Доступно для пользователей, находящихся в группе',
    'parameters': [
        roommates_group_purchases_fields,
        roommates_group_fields,
        roommates_group_users_fields,
        purchase_product_fields,
        purchase_product_category_fields
    ],
    'responses': {
        200: AllGroupsPurchasesSerializer
    }
}
