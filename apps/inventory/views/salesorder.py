from django.shortcuts import get_object_or_404

from apps.common.views.api.base import AppAPIView
from apps.common.views.api.generic import AppModelCUDAPIViewSet, AppModelListAPIViewSet
from apps.inventory.models.product import Product
from apps.inventory.models.salesorder import Cart, CartItem, WishList
from apps.inventory.serializer.salesorder import WishListRetriveSerializer, WishlistCUDSerializer


class AddProductWishListCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete product wishlist"""
    
    serializer_class = WishlistCUDSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a wishlist entry for a product.
        User ID will be retrieved from `request.user`.
        Product ID will be retrieved from the URL parameters.
        """
        
        user = request.user  
        product_id = kwargs.get('product_id') 
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return self.send_error_response(data={"Product not found"})        
        if WishList.objects.filter(user=user, product=product).exists():
            return self.send_error_response(data={"alredy added to your wishlist"})
        
        wishlist_entry = WishList.objects.create(user=user, product=product)
        return self.send_response(data={"added to your wishlist"})
 
    def destroy(self, request, *args, **kwargs):
        """
        Remove a specific product from the wishlist.
        User ID will be retrieved from `request.user`.
        Product ID will be retrieved from the URL parameters.
        """
        
        user = request.user
        product_id = kwargs.get('product_id')
        product = Product.objects.filter(id=product_id).first()

        if not product:
            return self.send_error_response(data={ "Product not found"})
        
        wishlist_entry = WishList.objects.filter(user=user, product=product).first()
        if not wishlist_entry:
            return self.send_error_response(data={"Product not found in your wishlist"})
        
        wishlist_entry.delete()
        return self.send_response(data={"Product removed from your wishlist"})    


class UserWishListRetrieveViewSet(AppModelListAPIViewSet):
    """A UserWishListRetrieveViewSet that provides `retrieve` action..."""
    
    serializer_class = WishListRetriveSerializer
    
    def get_queryset(self):
        """Override get_queryset() """

        user = self.request.user  
        return WishList.objects.filter(user=user)
       
       
class MoveWishListToCartView(AppAPIView):
    """API view to move items from the wishlist to the shopping cart."""

    def post(self, request):
        """Create function to convert product in wishlist to cart"""   
        
        user = request.user
        product_id = request.data.get("product_id")
        product = Product.objects.filter(id=product_id).first()
        wishlist_item = get_object_or_404(WishList, user=user, product=product)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        wishlist_item.delete()
        return self.send_response(data={"Product moved from your wishlist to shoppingcart"})