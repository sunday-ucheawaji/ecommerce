from rest_framework import serializers
from order.models.order import Order, OrderItem
from order.models.store import Store
from order.models.cart import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):

    cart_items = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = "__all__"


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
