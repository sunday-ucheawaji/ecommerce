from rest_framework import serializers
from user_auth.models.custom_user import CustomUser
from django.conf import settings



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=4, write_only=True, style={
                                     "input_type": "password"})
    confirm_password = serializers.CharField(max_length=30, min_length=4, write_only=True, style={
        "input_type": "password"})


    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        keys = list(dict(validated_data).keys())
        keys.remove("confirm_password")
        user_dict = {key: validated_data.get(key) for key in keys}
        if (validated_data.get("user_type") == "superuser") and (validated_data.get("email") not in settings.MANAGER):
            raise serializers.ValidationError(f"{validated_data.get('email')} cannot be a superuser")
        if validated_data.get("email") in settings.MANAGER:
            user = CustomUser.objects.create_superuser(**user_dict)
        else:
            user = CustomUser.objects.create_user(**user_dict)
        user.set_password(user_dict["password"])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name",
                  "email", "phone",  "user_type", "full_name", "password", "confirm_password"]
        read_only_fields = ["full_name"]


class VerifySerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30, min_length=4, style={
                                     "input_type": "password"}, write_only=True)
    class Meta:
        model =CustomUser
        fields = []


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=4, style={
                                     "input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "token", "full_name"]
        read_only_fields = ["full_name", "token"]


class LogoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["email", "token", ]
        read_only_fields = ["email", "token"]


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.IntegerField()

    password = serializers.CharField(max_length=30, min_length=4, style={
                                     "input_type": "password"})
    confirm_password = serializers.CharField(max_length=30, min_length=4, write_only=True, style={
        "input_type": "password"})
    
    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
   
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=30, min_length=4,  style={
                                     "input_type": "password"})
    new_password = serializers.CharField(max_length=30, min_length=4,  style={
        "input_type": "password"})
    confirm_password = serializers.CharField(max_length=30, min_length=4, write_only=True, style={
        "input_type": "password"})


class DeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["email"]
