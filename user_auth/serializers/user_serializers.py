from rest_framework import serializers
from user_auth.models.custom_user import CustomUser
from user_auth.models.staff import Staff
from product.serializers import ProductSerializer
from order.serializers import OrderSerializer
from django.conf import settings


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
                  "email", "phone", "password", "user_type", "full_name", "is_superuser", "otp"]
        read_only_fields = ["id", "full_name"]


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
