from rest_framework.exceptions import PermissionDenied

from apps.acess.choices import RoleTypeChoices
from apps.common.views.api.generic import AppModelCUDAPIViewSet, AppModelListAPIViewSet
from apps.inventory.models.category import Category, SubCategory
from apps.inventory.serializer.category import (
    CategoryRetriveSerializer,
    CategorySerializer,
    SubCategoryRetriveSerializer,
    SubCategorySerializer,
)


class CategoryCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete categories..."""

    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        """Override the create method to enforce role-based permission for creating categories..."""

        user = self.get_user()
        if user.role == RoleTypeChoices.admin:
            return super().create(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to create a category.")

    def get_queryset(self):
        """Override get_queryset()..."""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return Category.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class CategoryListView(AppModelListAPIViewSet):
    """Api viewset to list all categories..."""

    serializer_class = CategoryRetriveSerializer

    def get_queryset(self):
        """Override get_queryset()..."""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return Category.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class SubCategoryCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete subcategories..."""

    serializer_class = SubCategorySerializer

    def create(self, request, *args, **kwargs):
        """Override the create..."""

        user = request.user
        if user.role == RoleTypeChoices.admin:
            return super().create(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to create a SubCategory.")

    def get_queryset(self):
        """Override get_queryset()..."""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return SubCategory.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class SubCategoryListView(AppModelListAPIViewSet):
    """Api viewset to list all categories"""

    serializer_class = SubCategoryRetriveSerializer

    def get_queryset(self):
        """Override get_queryset()..."""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return SubCategory.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this content.")
