from rest_framework.permissions import BasePermission


"""
Custom permission to only allow users who are:
- Superuser
- Active
- Staff
"""
class IsSuperuserActiveStaff(BasePermission):
  def has_permission(self, request, view):
    user = request.user
    return user and user.is_authenticated and user.is_superuser and user.is_active and user.is_staff
