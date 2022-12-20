from typing import Any, Optional, Iterable, Sequence, Type

from django.db.models import Model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import Field
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer, Serializer


class StrMethodMixin:

    def __str__(self) -> str:
        return self.name


class DynamicFieldsSerializerMixin:
    """Примесь к сериализаторам, позволяющая динамически изменять требуемые в ответе поля"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        DynamicFieldsSerializerMixin.__doc__ = None
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        self.change_fields(fields)

    def change_fields(self, fields: Iterable) -> None:
        if fields is None:
            return
        existing, allowed = set(self.fields), set(fields)
        for field in existing - allowed:
            self.fields.pop(field)


class GetObjectByIdFromRequestSerializerMixin:
    """
    Примесь к сериализаторам, позволяющая пропустить валидацию объекта
    при создании связанного с ним другого объекта.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        GetObjectByIdFromRequestSerializerMixin.__doc__ = None
        self.validate_by_id = kwargs.pop('validate_by_id', False)
        super().__init__(*args, **kwargs)

    @staticmethod
    def val(data: Any) -> None:
        if type(data) is not int:
            raise ValidationError('Поле должно быть integer')

    def get_obj(self, pk: int) -> Model:
        return get_obj_by_pk(self.Meta.model, pk)

    def to_internal_value(self, data: Any) -> Model:
        if not self.validate_by_id:
            return super().to_internal_value(data)
        self.val(data)
        return self.get_obj(data)


class ChangeFieldsInDeepSerializersMixin:
    """Примесь к сериализаторам, позволяющая изменять поля сериализаторов-полей"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ChangeFieldsInDeepSerializersMixin.__doc__ = None
        query_fields_for_many_serializers = self.get_query_fields(kwargs)
        super().__init__(*args, **kwargs)
        self.change_fields_in_depth_serializer(query_fields_for_many_serializers)

    def change_fields_in_depth_serializer(self,
                                          query_fields_for_many_serializers: dict[str, Optional[Sequence]]) -> None:
        for query_name, serializers_fields in self.Meta.fields_serializer_data:
            query_fields_for_one_serializer = query_fields_for_many_serializers.pop(query_name, None)
            if query_fields_for_one_serializer is None:
                continue
            change_fields_in_depth_serializer(serializers_fields, query_fields_for_one_serializer, self)

    def get_query_fields(self, init_kwargs: dict[str, Any]) -> dict[str, Optional[Sequence]]:
        return {field: init_kwargs.pop(field, None) for field, _ in self.Meta.fields_serializer_data}


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


def get_field_handler(field_name: str, main_serializer: Serializer) -> Optional[Field | Serializer]:
    """Функция, возвращающая обработчик (Field или Serializer) для данного поля"""

    if field_name not in main_serializer.fields:
        return None
    field_handler = main_serializer.fields[field_name]
    if isinstance(field_handler, ListSerializer):
        field_handler = field_handler.child
    return field_handler


def change_fields_in_serializer(serializer_field: str, required_fields: Iterable,
                                main_serializer: Serializer) -> None:
    """Функция, изменяющая все поля вложенного сериализатора на требуемые при его наличии"""

    field_handler = get_field_handler(serializer_field, main_serializer)
    if not isinstance(field_handler, DynamicFieldsSerializerMixin):
        return
    field_handler.change_fields(required_fields)


def change_fields_in_depth_serializer(serializer_fields: Sequence, required_fields: Iterable,
                                      main_serializer: Serializer) -> None:
    """Функиця, изменяющая все поля вложенного на некоторую глубину сериализатора на требуемые при его наличии"""

    for serializer_field in serializer_fields[:-1]:
        main_serializer = get_field_handler(serializer_field, main_serializer)
        if not isinstance(main_serializer, Serializer):
            return
    change_fields_in_serializer(serializer_fields[-1], required_fields, main_serializer)


def get_obj_by_pk(m: Type[Model], pk: int) -> Model:
    """Функция, возвращающая объект, если он существует"""

    obj = m.objects.filter(pk=pk)
    if not obj.exists():
        raise ValidationError('Такой объект не существует')
    return obj[0]
