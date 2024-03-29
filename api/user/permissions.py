from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, user): #type: ignore
        if request.user:
            return user == request.user
        return False
