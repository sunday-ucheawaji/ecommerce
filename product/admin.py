from django.contrib import admin
from product.models.category import Category, Brand, Stock
from product.models.product_model import Product
from product.models.review import Review

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Stock)
admin.site.register(Product)
admin.site.register(Review)
