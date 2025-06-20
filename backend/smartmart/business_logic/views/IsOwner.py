

from rest_framework.permissions import IsAuthenticated

class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        """
        Permission to only allow owners of an object to edit it.
        """
        return obj == request.user
