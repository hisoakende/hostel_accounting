from rest_framework import serializers

from accounts.models import User
from utils import DynamicFieldsMixinModelSerializer


class UserSerializer(DynamicFieldsMixinModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_superuser', 'is_staff', 'date_joined', 'last_login')
