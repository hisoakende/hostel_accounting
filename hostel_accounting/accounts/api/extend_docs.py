import extend_docs_global

"""UserViewSet"""

user_retrieve = {
    'summary': 'Получить пользователя',
    'description': 'Доступно для администраторов и для пользователя-владельца данных',
    'parameters': [
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
        extend_docs_global.page_param_ru,
        extend_docs_global.page_size_param_ru
    ]
}
