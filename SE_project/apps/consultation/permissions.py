from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_advisor


class IsAdviser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_advisor
