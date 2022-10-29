from rest_framework import serializers
from product.models.product_model import Product
from product.models.category import Category, Brand, Stock
from order.serializers import OrderItemSerializer


class StockSerializer(serializers.ModelSerializer):

    # product = serializers.StringRelatedField(required=True, read_only=False)
    store = serializers.StringRelatedField()

    class Meta:
        model = Stock
        fields = ["id", "quantity", "product", "store"]


class ProductSerializer(serializers.ModelSerializer):

    stock = StockSerializer(required=True)

    class Meta:
        model = Product
        fields = ["product_name", "model_year", "list_price",
                  "brand", "category", "supplier", "stock"]


class CategorySerializer(serializers.ModelSerializer):

    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):

    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Brand
        fields = "__all__"
