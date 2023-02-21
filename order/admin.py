from django.contrib import admin
from order.models.order import Order, OrderItem
from order.models.store import Store
from order.models.cart import Cart, CartItem


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Store)
admin.site.register(Cart)
admin.site.register(CartItem)
