from typing import Any, Optional, Iterable

from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class DynamicFieldsMixinModelSerializer(serializers.ModelSerializer):
    """Примесь к сериализаторам, позволяющая динамически изменять требуемые в ответе поля"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is None:
            return
        existing, allowed = set(self.fields), set(fields)
        for field in existing - allowed:
            self.fields.pop(field)


def get_all_fields_from_request(request: Request, fields_params: Iterable = ('fields',)) -> dict[str, list[str]]:
    """
    Функция возвращает требуемые для сериализации поля из параметров запроса
    для модели и связанных с ней других моделей
    """

    def get_fields_from_request(fields_param: str = 'fields') -> Optional[list[str]]:
        """Функция возвращает требуемые для сериализации поля из параметров запроса для одной модели"""

        fields = request.query_params.get(fields_param)
        if fields is None:
            return None
        return fields.split(',')

    return {param: get_fields_from_request(param) for param in fields_params}


def get_default_retrieve_response(request: Request, view: GenericAPIView,
                                  fields_params: Iterable = ('fields',)) -> Response:
    """Функция возвращает стандартный для большинства представлений retrieve ответ"""

    fields_params = get_all_fields_from_request(request, fields_params)
    serializer = view.serializer_class(view.get_object(), **fields_params)
    return Response(serializer.data)


def get_default_list_response_with_pagination(request: Request, view: GenericAPIView,
                                              fields_params: Iterable = ('fields',)) -> Response:
    """Функция возвращает стандартный для большинства представлений list ответ с пагинацией"""

    if not view.queryset:
        return Response(status=status.HTTP_404_NOT_FOUND)
    fields_params = get_all_fields_from_request(request, fields_params)
    page = view.paginate_queryset(view.queryset)
    serializer = view.serializer_class(page, many=True, **fields_params)
    return view.get_paginated_response(serializer.data)
