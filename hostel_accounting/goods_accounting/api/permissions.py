from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.method in permissions.SAFE_METHODS
