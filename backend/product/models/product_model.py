from django.db import models
from user_auth.models.supplier import Supplier
from product.models.category import Category, Brand


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    model_year = models.DateField()
    list_price = models.IntegerField()
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.product_name
