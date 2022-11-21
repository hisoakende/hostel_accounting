from typing import Any, Optional

from rest_framework import serializers
from rest_framework.request import Request


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is None:
            return
        existing, allowed = set(self.fields), set(fields)
        for field in existing - allowed:
            self.fields.pop(field)


def get_fields_from_request(request: Request, fields_name: str = 'fields') -> Optional[list[str]]:
    fields = request.query_params.get(fields_name)
    if fields is None:
        return None
    return fields.split(',')
