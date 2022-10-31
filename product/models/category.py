from django.db import models
# from product.models.product_model import Product
from order.models.store import Store


class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=30)

    def __str__(self):
        return self.brand_name


class Stock(models.Model):
    quantity = models.IntegerField()
    product = models.OneToOneField(
        "product.Product", on_delete=models.CASCADE, related_name="stock")
    store = models.OneToOneField(
        Store, on_delete=models.CASCADE, related_name="stock")

    def __str__(self):
        return f"Stock: {self.product} - {self.quantity} "
