from apps.acess.choices import RoleTypeChoices
from apps.common.permission_class import RoleBasedPermission
from apps.common.views.api.generic import AppModelCUDAPIViewSet, AppModelListAPIViewSet, AppModelRetrieveAPIViewSet
from apps.inventory.models.product import Image, Offer, Product, Specification
from apps.inventory.models.salesorder import RatingReview
from apps.inventory.serializer.product import (
    ImageReadSerializer,
    ProducImageSerializer,
    ProductReadSerializer,
    ProductSpecificationSerializer,
    ProductWriteSerializer,
    RatingReviewSerializer,
    SpecificationRetriveSerializer,
    SpecificationSerializer,
    productOfferWriteSerializer,
)


class ProductCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete products"""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = ProductWriteSerializer
    queryset = Product.objects.filter(is_deleted=False)


class RetriveProductListViewSet(AppModelListAPIViewSet):
    """Api viewset to retrieve product details"""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = ProductReadSerializer
    queryset = Product.objects.filter(is_deleted=False)
    search_fields = ["name", "description", "sub_category__name"]
    filterset_fields = ["sub_category__name", "final_price", "discount", "available_stock"]
    ordering_fields = ["final_price", "discount", "available_stock"]
    ordering = ["name"]


class RetriveProductViewSet(AppModelRetrieveAPIViewSet):
    """Api viewset to retrieve product details"""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin, RoleTypeChoices.member]
    serializer_class = ProductReadSerializer
    queryset = Product.objects.filter(is_deleted=False)


class ProductImageCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete product images"""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = ProducImageSerializer
    queryset = Image.objects.all()

    def create(self, request, *args, **kwargs):
        """Overridden the create method"""

        product_id = request.data.get("product")
        images = request.FILES.getlist("image")
        product = Product.objects.get(id=product_id)
        for image in images:
            Image.objects.create(product=product, image=image)
        return self.send_response(data="Image saves successfully...")


class ProductImageListReviewViewSet(AppModelListAPIViewSet):
    """Api viewset to retrieve product images"""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = ImageReadSerializer
    queryset = Image.objects.all()


class ProductImageReviewViewSet(AppModelRetrieveAPIViewSet):
    """Api viewset to retrieve product image"""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = ImageReadSerializer
    queryset = Image.objects.all()


class ProductOffersCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete product offers"""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = productOfferWriteSerializer
    queryset = Offer.objects.all()


class SpecificationCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete specifications"""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = SpecificationSerializer
    queryset = Specification.objects.all()


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

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = ProductSpecificationSerializer


class RatingReviewViewSet(AppModelCUDAPIViewSet):
    """ViewSet for Rating and Review"""

    queryset = RatingReview.objects.all()
    serializer_class = RatingReviewSerializer

    def perform_create(self, serializer):
        """Assign the current user to the review during creation."""

        serializer.save(user=self.get_user())
