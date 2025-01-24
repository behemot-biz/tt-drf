from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow owners to edit objects and
    others to only read.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'owner'):  # Direct ownership
            return obj.owner == request.user
        elif hasattr(obj, 'recipe') and hasattr(obj.recipe, 'owner'):
            return obj.recipe.owner == request.user

        return False
