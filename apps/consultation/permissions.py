from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not request.user.is_advisor


class IsAdviser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_advisor
