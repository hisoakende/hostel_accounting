from rest_framework import serializers

from accounts.models import User, RoommatesGroup
from utils import DynamicFieldsSerializerMixin, GetObjectByIdFromRequestSerializerMixin, \
    ChangeFieldsInDeepSerializersMixin


class UserSerializerWithoutRoommatesGroup(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_superuser', 'is_staff', 'date_joined', 'last_login')


class RoommatesGroupSerializerWithoutUsers(GetObjectByIdFromRequestSerializerMixin, DynamicFieldsSerializerMixin,
                                           serializers.ModelSerializer):
    class Meta:
        model = RoommatesGroup
        fields = ('id', 'name', 'created_at')


class UserSerializer(ChangeFieldsInDeepSerializersMixin, GetObjectByIdFromRequestSerializerMixin,
                     DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    roommates_group = RoommatesGroupSerializerWithoutUsers(validate_by_id=True, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'roommates_group', 'email', 'first_name',
                  'last_name', 'is_superuser', 'is_staff', 'date_joined', 'last_login')
        fields_serializer_data = (('roommates_group_fields', ('roommates_group',)),)


class RoommatesGroupSerializer(ChangeFieldsInDeepSerializersMixin, DynamicFieldsSerializerMixin,
                               serializers.ModelSerializer):
    users = UserSerializerWithoutRoommatesGroup(many=True, read_only=True)

    class Meta:
        model = RoommatesGroup
        fields = ('id', 'name', 'created_at', 'users')
        fields_serializer_data = (('users_fields', ('users',)),)
