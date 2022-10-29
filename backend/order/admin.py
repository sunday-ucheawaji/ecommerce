from django.contrib import admin
from order.models.order import Order, OrderItem
from order.models.store import Store


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Store)
