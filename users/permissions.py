from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    message = "Вы не являетесь модератором."

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name="moders").exists())


class isOwner(BasePermission):
    message = "Вы не являетесь владельцем."

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
