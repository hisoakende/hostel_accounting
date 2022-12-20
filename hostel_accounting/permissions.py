from typing import Any

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from accounts.models import User
from goods_accounting.models import Purchase


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.method in permissions.SAFE_METHODS


class IsThisUser(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return 'pk' in view.kwargs

    def has_object_permission(self, request: Request, view: APIView, obj: User) -> bool:
        return obj == request.user


class IsOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.method in ('DELETE', 'PUT', 'PATCH')

    def has_object_permission(self, request: Request, view: APIView, obj: Purchase) -> bool:
        return Purchase.user == request.user


class PurchasePermissionGET(permissions.BasePermission):

    def has_permission(self, request: Request, view: APIView) -> bool:
        return IsAuthenticated.has_permission(self, request, view)

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        return request.user.roommates_group == obj.user.roommates_group or request.user.is_staff


class PurchasePermission(permissions.BasePermission):
    """Класс, который обработывает разрешения для покупок"""

    permissions = {'GET': (PurchasePermissionGET,), 'POST': (IsAuthenticated,), 'DELETE': (IsOwner, IsAdminUser)}

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method not in self.permissions:
            return True
        return any(p.has_permission(self, request, view) for p in self.permissions[request.method])

    def has_object_permission(self, request: Request, view: APIView, obj: Purchase) -> bool:
        return any(p.has_object_permission(self, request, view, obj) for p in self.permissions[request.method])
