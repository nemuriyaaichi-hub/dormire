from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return self.is_admin(request)

    def is_admin(self, request):
        return request.user.is_superuser


class IsCrowdFundingUser(BasePermission):
    def has_permission(self, request, view):
        return self.is_crowdfunding_user(request)

    def is_crowdfunding_user(self, request):
        return request.user.is_crowdfunding_user


class IsFurusatoTaxUser(BasePermission):
    def has_permission(self, request, view):
        return self.is_furusato_tax_user(request)

    def is_furusato_tax_user(self, request):
        return request.user.is_furusato_tax_user


class IsSalonUser(BasePermission):
    def has_permission(self, request, view):
        return self.is_salon_user(request)

    def is_salon_user(self, request):
        return request.user.is_salon_user
