from django.conf import settings
from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from user_auth.models.custom_user import CustomUser
from user_auth.utils import generateOTP


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
            raise serializers.ValidationError(
                f"{validated_data.get('email')} cannot be a superuser")
        if validated_data.get("email") in settings.MANAGER:
            user = CustomUser.objects.create_superuser(**user_dict)
        else:
            user = CustomUser.objects.create_user(**user_dict)
        otp = generateOTP()
        user.otp = otp
        user.set_password(user_dict["password"])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name",
                  "email", "phone",  "user_type", "full_name",  "password", "confirm_password"]
        read_only_fields = ["full_name"]


class VerifySerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ["email", "otp"]


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.IntegerField()

    password = serializers.CharField(max_length=30, min_length=4, style={
                                     "input_type": "password"})
    confirm_password = serializers.CharField(max_length=30, min_length=4, write_only=True, style={
        "input_type": "password"})

    email = serializers.EmailField()

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

    def validate(self, data):

        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError(
                "Old password is the same as new password. Please use a new password")
        if data['confirm_password'] != data['new_password']:
            raise serializers.ValidationError(
                "Passwords do not match")
        return data


class DeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["email"]


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
