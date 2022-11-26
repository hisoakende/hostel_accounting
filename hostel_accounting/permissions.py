from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from accounts.models import User


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.method in permissions.SAFE_METHODS


class IsThisUser(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return 'pk' in view.kwargs

    def has_object_permission(self, request: Request, view: APIView, obj: User) -> bool:
        return obj == request.user
