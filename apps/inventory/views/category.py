from apps.acess.choices import RoleTypeChoices
from apps.common.permission_class import RoleBasedPermission
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

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryListView(AppModelListAPIViewSet):
    """Api viewset to list all categories..."""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = CategoryRetriveSerializer
    queryset = Category.objects.all()


class SubCategoryCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete subcategories..."""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


class SubCategoryListView(AppModelListAPIViewSet):
    """Api viewset to list all categories"""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = SubCategoryRetriveSerializer
    queryset = SubCategory.objects.all()
