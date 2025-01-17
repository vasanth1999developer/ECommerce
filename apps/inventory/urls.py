from django.urls import path

from apps.common.routers import AppSimpleRouter
from apps.inventory.views.category import (
    CategoryCUDViewSet,
    CategoryListView,
    SubCategoryCUDViewSet,
    SubCategoryListView,
)
from apps.inventory.views.product import (
    ProductCUDViewSet,
    ProductImageCUDViewSet,
    ProductImageListReviewViewSet,
    ProductImageReviewViewSet,
    ProductOffersCUDViewSet,
    ProductSpecificationCUDApiViewSet,
    RatingReviewViewSet,
    RetriveProductListViewSet,
    RetriveProductViewSet,
    SpecificationCUDViewSet,
    SpecificationListViewSet,
)
from apps.inventory.views.salesorder import (
    AddProductWishListCUDViewSet,
    CartOfferSelectingViewSet,
    CartRetriveForUserViewSet,
    MoveWishListToCartView,
    OrderCUDApiViewSet,
    UserWishListRetrieveViewSet,
)
from apps.inventory.views.webhook import razorpay_webhook

API_URL_PREFIX = "v1/inventory/"

router = AppSimpleRouter()

# Category API
router.register(f"{API_URL_PREFIX}category", CategoryCUDViewSet, basename="category")
router.register(f"{API_URL_PREFIX}list-category", CategoryListView, basename="category-list")

# SubCategory API
router.register(f"{API_URL_PREFIX}subcategory", SubCategoryCUDViewSet, basename="subcategory")
router.register(f"{API_URL_PREFIX}list-subcategory", SubCategoryListView, basename="subcategory-list")

# Product API
router.register(f"{API_URL_PREFIX}product", ProductCUDViewSet, basename="product")
router.register(f"{API_URL_PREFIX}product-image", ProductImageCUDViewSet, basename="product-image")
router.register(f"{API_URL_PREFIX}get-products", RetriveProductListViewSet, basename="get-products")
router.register(f"{API_URL_PREFIX}get-product", RetriveProductViewSet, basename="get-product")
router.register(f"{API_URL_PREFIX}get-product-images", ProductImageReviewViewSet, basename="get-product-images")
router.register(f"{API_URL_PREFIX}get-images", ProductImageListReviewViewSet, basename="get-images")

# Offer API
router.register(f"{API_URL_PREFIX}offers", ProductOffersCUDViewSet, basename="offer")

# Specification API
router.register(f"{API_URL_PREFIX}Specification", SpecificationCUDViewSet, basename="Specification")

# ProductSpecification API
router.register(
    f"{API_URL_PREFIX}product-specification", ProductSpecificationCUDApiViewSet, basename="product-specification"
)

# Wishlist API
router.register(f"{API_URL_PREFIX}wishlist-list", UserWishListRetrieveViewSet, basename="wishlist-list")

# Cart API
router.register(f"{API_URL_PREFIX}cart-list", CartRetriveForUserViewSet, basename="cart-list")
router.register(f"{API_URL_PREFIX}update-cart-items-offer", CartOfferSelectingViewSet, basename="update-offer")

# Order API
router.register(f"{API_URL_PREFIX}orders", OrderCUDApiViewSet, basename="order")

# rating API
router.register(f"{API_URL_PREFIX}rating-reviews", RatingReviewViewSet, basename="rating-review")

urlpatterns = [
    path(
        f"{API_URL_PREFIX}get-specifications/",
        SpecificationListViewSet.as_view({"get": "list"}),
        name="specifications_list",
    ),
    path(
        f"{API_URL_PREFIX}wishlist/<int:product_id>/",
        AddProductWishListCUDViewSet.as_view(
            {
                "post": "create",
                "delete": "destroy",
            }
        ),
    ),
    path(f"{API_URL_PREFIX}add-to-cart", MoveWishListToCartView.as_view(), name="add-to-cart"),
    path("razorpay/webhook/", razorpay_webhook, name="razorpay_webhook"),
] + router.urls
