from django.db import models
from user_auth.models.customer import Customer
# from user_auth.models.staff import Staff
from product.models.product_model import Product
from order.models.store import Store


class Order(models.Model):

    STATUS = (
        ("pending", "pending"),
        ("processing", "processing"),
        ("rejected", "rejected"),
        ("completed", "completed")
    )
    order_status = models.CharField(
        max_length=20, choices=STATUS, default="pending")
    order_date = models.DateTimeField(auto_now_add=True)
    required_date = models.DateTimeField()
    shipped_date = models.DateTimeField()
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="orders")
    staff = models.ForeignKey(
        "user_auth.Staff", on_delete=models.CASCADE, related_name="orders")
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order {self.order_status} {self.customer}"


class OrderItem(models.Model):
    quantity = models.IntegerField(default=0)
    list_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items")

    def __str__(self):
        return f"{self.product} {self.quantity}"
