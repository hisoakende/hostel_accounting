from rest_framework import serializers

from accounts.models import User
from utils import DynamicFieldsSerializerMixin, GetObjectByIdFromRequestSerializerMixin


class UserSerializer(GetObjectByIdFromRequestSerializerMixin, DynamicFieldsSerializerMixin,
                     serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'roommates_group', 'email', 'first_name',
                  'last_name', 'is_superuser', 'is_staff', 'date_joined', 'last_login')
