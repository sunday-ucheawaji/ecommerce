from django.db import models
from user_auth.models.custom_user import CustomUser
from product.models.product_model import Product


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="carts")

    def __str__(self):
        return f"Cart for {self.user.full_name}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(default=0)
    list_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in cart for {self.cart.user.full_name}"
