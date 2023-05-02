from django.db.models import Model
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSetMixin


class AuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of an object to perform write operations.
    """

    def has_object_permission(
        self, request: Request, view: ViewSetMixin, obj: Model
    ) -> bool:
        # Read permissions are allowed to any request
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.author == request.user
