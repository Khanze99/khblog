from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner this object."
    my_save_method = ['GET', 'PUT']

    def has_permission(self, request, view):
        if request.method in self.my_save_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user