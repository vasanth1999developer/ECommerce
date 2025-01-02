from rest_framework.exceptions import PermissionDenied

from apps.acess.choices import RoleTypeChoices
from apps.common.views.api.generic import AppModelCUDAPIViewSet, AppModelListAPIViewSet, AppModelRetrieveAPIViewSet
from apps.inventory.models.product import Image, Offer, Product, Specification
from apps.inventory.serializer.product import (
    ImageReadSerializer,
    ProducImageSerializer,
    ProductReadSerializer,
    ProductSpecificationSerializer,
    ProductWriteSerializer,
    SpecificationRetriveSerializer,
    SpecificationSerializer,
    productOfferWriteSerializer,
)


class ProductCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete products"""

    serializer_class = ProductWriteSerializer

    def create(self, request, *args, **kwargs):
        """Overridden to create function..."""

        user = self.get_user()
        if user.role == RoleTypeChoices.admin:
            return super().create(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to view this content.")

    def get_queryset(self):
        """Override get_queryset()..."""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return Product.objects.filter(is_deleted=False)
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class RetriveProductListViewSet(AppModelListAPIViewSet):
    """Api viewset to retrieve product details"""

    serializer_class = ProductReadSerializer

    def get_queryset(self):
        """Override get_queryset()..."""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return Product.objects.filter()
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class RetriveProductListForBuyersViewSet(AppModelListAPIViewSet):
    """Api viewset to retrieve product details for buyers with filters, search and sort"""

    serializer_class = ProductReadSerializer
    queryset = Product.objects.all()
    search_fields = ["name", "description", "sub_category__name"]
    filterset_fields = ["sub_category__name", "final_price", "discount", "available_stock"]
    ordering_fields = ["name", "final_price", "discount", "available_stock"]
    ordering = ["name"]


class RetriveProductViewSet(AppModelRetrieveAPIViewSet):
    """Api viewset to retrieve product details"""

    serializer_class = ProductReadSerializer

    def get_queryset(self):
        """Override get_queryset()..."""

        user = self.request.user
        allowed_roles = [RoleTypeChoices.admin, RoleTypeChoices.member]
        if user.role in allowed_roles:
            return Product.objects.filter()
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class ProductImageCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete product images"""

    serializer_class = ProducImageSerializer

    def create(self, request, *args, **kwargs):
        """Overridden the create method"""

        user = self.get_user()
        allowed_roles = [RoleTypeChoices.admin]
        if user.role in allowed_roles:
            product_id = request.data.get("product")
            images = request.FILES.getlist("image")
            product = Product.objects.get(id=product_id)
            for image in images:
                Image.objects.create(product=product, image=image)
            return self.send_response(data="Image saves successfully...")
        raise PermissionDenied("You do not have permission to create a category.")

    def get_queryset(self):
        """Override get_queryset()"""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return Image.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class ProductImageListReviewViewSet(AppModelListAPIViewSet):
    """Api viewset to retrieve product images"""

    serializer_class = ImageReadSerializer

    def get_queryset(self):
        """Override get_queryset()"""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return Image.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class ProductImageReviewViewSet(AppModelRetrieveAPIViewSet):
    """Api viewset to retrieve product image"""

    serializer_class = ImageReadSerializer

    def get_queryset(self):
        """return image based on id"""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return Image.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class ProductOffersCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete product offers"""

    serializer_class = productOfferWriteSerializer

    def create(self, request, *args, **kwargs):
        """Overridden to create function"""

        user = self.get_user()
        if user.role == RoleTypeChoices.admin:
            return super().create(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to create a category.")

    def get_queryset(self):
        """Override get_queryset()..."""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return Offer.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class SpecificationCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete specifications"""

    serializer_class = SpecificationSerializer

    def create(self, request, *args, **kwargs):
        """Override create()..."""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return super().create(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to view this content.")

    def get_queryset(self):
        """Override get_queryset()..."""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return Specification.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class SpecificationListViewSet(AppModelListAPIViewSet):
    """ViewSet to retrieve specifications based on sub_category_id."""

    queryset = Specification.objects.all()
    serializer_class = SpecificationRetriveSerializer

    def get_queryset(self):
        """Override get_queryset()..."""
        user = self.request.user
        if user.role != RoleTypeChoices.admin:
            return self.queryset.none()
        sub_category_id = self.request.query_params.get("sub_category_id")
        if sub_category_id:
            return self.queryset.filter(sub_category_id=sub_category_id)
        return self.queryset.none()


class ProductSpecificationCUDApiViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete product specifications"""

    serializer_class = ProductSpecificationSerializer

    def create(self, request, *args, **kwargs):
        """Override create()"""

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return super().create(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to view this content.")
