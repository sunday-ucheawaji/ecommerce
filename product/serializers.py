from rest_framework import serializers
from product.models.product_model import Product
from product.models.category import Category, Brand, Stock
from order.serializers import OrderItemSerializer
from product.models.review import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["product_name", "model_year", "list_price", "product_image",
                  "brand", "category", "supplier", "stock"]
        read_only_fields = ["stock"]


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ["id", "quantity", "product", "store"]


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
