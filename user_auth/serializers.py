from rest_framework import serializers
from user_auth.models.custom_user import CustomUser
from user_auth.models.customer import Customer
from user_auth.models.supplier import Supplier
from user_auth.models.staff import Staff
from product.serializers import ProductSerializer
from order.serializers import OrderSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=4, write_only=True, style={
                                     "input_type": "password"})

    def validate_user_type(self, value):
        if value == "superuser":
            raise serializers.ValidationError(
                "User type cannot be a superuser")
        return value

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name",
                  "email", "phone", "password", "user_type", "full_name"]
        read_only_fields = ["full_name"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=4, write_only=True, style={
                                     "input_type": "password"})
    confirm_password = serializers.CharField(max_length=30, min_length=4, write_only=True, style={
        "input_type": "password"})

    def validate_user_type(self, value):
        if value == "superuser":
            raise serializers.ValidationError(
                "User type cannot be a superuser")
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        keys = list(dict(validated_data).keys())
        keys.remove("confirm_password")
        user_dict = {key: validated_data.get(key) for key in keys}
        user = CustomUser.objects.create_user(**user_dict)
        user.set_password(user_dict["password"])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name",
                  "email", "phone",  "user_type", "full_name", "password", "confirm_password"]
        read_only_fields = ["full_name"]


class CustomerSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer(write_only=True)

    def create(self, validated_data):
        custom_user_dict = validated_data.get('custom_user')
        custom_user_instance = CustomUser.objects.create_user(
            **custom_user_dict)
        keys = list(dict(validated_data).keys())
        keys.remove("custom_user")
        customer_dict = {key: validated_data.get(key) for key in keys}
        customer_dict["custom_user"] = custom_user_instance
        customer_instance = Customer.objects.create(**customer_dict)
        return customer_instance

    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["full_name"]


class SupplierSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer(write_only=True)

    def create(self, validated_data):
        custom_user_dict = validated_data.get('custom_user')
        custom_user_instance = CustomUser.objects.create_user(
            **custom_user_dict)
        keys = list(dict(validated_data).keys())
        keys.remove("custom_user")
        supplier_dict = {key: validated_data.get(key) for key in keys}
        supplier_dict["custom_user"] = custom_user_instance
        supplier_instance = Customer.objects.create(**supplier_dict)
        return supplier_instance

    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ["full_name"]


class StaffSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer(write_only=True)

    def create(self, validated_data):
        custom_user_dict = validated_data.get('custom_user')
        custom_user_instance = CustomUser.objects.create_user(
            **custom_user_dict)
        keys = list(dict(validated_data).keys())
        keys.remove("custom_user")
        staff_dict = {key: validated_data.get(key) for key in keys}
        staff_dict["custom_user"] = custom_user_instance
        staff_instance = Staff.objects.create(**staff_dict)
        return staff_instance

    class Meta:
        model = Staff
        fields = "__all__"
        read_only_fields = ["manager", "store", "full_name"]


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=4, style={
                                     "input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "token", "full_name"]
        read_only_fields = ["full_name", "token"]


class LogoutSerializer(serializers.ModelSerializer):

    # def create(self, validated_data):

    class Meta:
        model = CustomUser
        fields = ["email", "token", ]
        read_only_fields = ["email", "token"]
