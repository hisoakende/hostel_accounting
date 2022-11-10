from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


class RequiredFieldsMixin:
    """
    Миксин, который добавляет конечную точку, возвращающую список полей,
    которые обязательны к заполнению при создании объекта
    """

    @action(detail=False, url_path='required-fields')
    def required_fields(self, request: Request) -> Response:
        return Response({'required_fields': self.model.user_required_fields})
