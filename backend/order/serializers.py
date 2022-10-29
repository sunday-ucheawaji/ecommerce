from rest_framework import serializers
from order.models.order import Order, OrderItem
from order.models.store import Store
# from product.serializers import StockSerializer
# from user_auth.serializers import StaffSerializer


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    order_items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(read_only=True, many=True)
    stock = serializers.StringRelatedField(read_only=True)
    staff = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Store
        fields = "__all__"
