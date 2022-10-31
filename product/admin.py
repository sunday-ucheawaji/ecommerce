from django.contrib import admin
from product.models.category import Category, Brand, Stock
from product.models.product_model import Product

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Stock)
admin.site.register(Product)
