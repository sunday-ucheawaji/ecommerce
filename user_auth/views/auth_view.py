from django.contrib.auth import authenticate
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from user_auth.serializers.user_serializers import CustomUserSerializer
from user_auth.serializers.auth_serializers import (
    RefreshTokenSerializer, ResetPasswordSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, RegisterSerializer, RegisterStaffSerializer,  VerifySerializer, DeleteSerializer)
from user_auth.models.custom_user import CustomUser
from user_auth.models.staff import Staff
from user_auth.utils import generateOTP
import time


class RegisterView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.data.get("email")
            full_name = serializer.data.get("full_name")
            user = CustomUser.objects.get(email=email)
            otp = user.otp
            subject = 'Welcome to Ecommerce world'
            message = f'Hi {full_name}, thank you for registering in ecommerce. Please confirm your account with this OTP- {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class RegisterStaffView(generics.CreateAPIView):
    permission_classes = ()
    queryset = Staff.objects.all()
    serializer_class = RegisterStaffSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            custom_user = serializer.data.get("custom_user")
            email = custom_user.get("email")
            full_name = custom_user.get("full_name")
            try:
                user = CustomUser.objects.get(email=email)
                otp = user.otp
                subject = 'Welcome to Ecommerce world'
                message = f'Hi {full_name}, thank you for registering in ecommerce. Please confirm your account with this OTP- {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_mail(subject, message, email_from, recipient_list)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist as e:
                return Response({"error": "User does not exist"})

        return Response(serializer.errors)


class VerifyView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = VerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            email = serializer.data.get("email")
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist as e:
                return Response({"msg": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            otp = serializer.data.get("otp")
            if user.otp != otp:
                return Response({"msg": "OTP is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            subject = 'Verification Successful'

            if user.is_active:
                message = f'Hi {user.full_name}, your account is already verified.'
                send_mail(subject, message, email_from, recipient_list)
                return Response({"msg": f"{user.full_name}, your account is already verified"}, status=status.HTTP_201_CREATED)

            user.is_active = True
            user.save()
            message = f'Hi {user.full_name}, your account has been verified.'
            send_mail(subject, message, email_from, recipient_list)
            return Response({"msg": "Verified! Registration successful"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class ForgotPasswordView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist as e:
            raise Response({"msg": "Email does not exist"},
                           status=status.HTTP_400_BAD_REQUEST)
        otp = generateOTP()
        user.otp = otp
        user.save()
        user_serialized = CustomUserSerializer(user)
        full_name = user_serialized.data.get("full_name")
        user_otp = user_serialized.data.get("otp")
        subject = 'OTP-Reset Password'
        message = f'Hi {full_name}, use OTP - {user_otp} to reset password.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
        return Response({"OTP": f"OTP sent to {email} to reset password"})


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                email = user.email
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                subject = 'Password Changed Successful'
                message = f'Hi {user.full_name}, your have successfully changed your password.'
                send_mail(subject, message, email_from, recipient_list)
                return Response({"msg": "Password changed successfully!"})
            return Response({"msg": "Incorrect Password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)


class ResetPasswordView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            otp = serializer.data.get("otp")
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist as e:
                return Response({"msg": "This email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            if otp != user.otp:
                return Response({"msg": "Incorrect OTP"}, status=status.HTTP_400_BAD_REQUEST)

            if user.check_password(password):
                return Response({"mesg": "This is an old Password! Set new password"})
            user.set_password(password)
            user.save()
            email = user.email
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            subject = 'Password Reset Successful'
            message = f'Hi {user.full_name}, your have successfully reset your password.'
            send_mail(subject, message, email_from, recipient_list)
            return Response({"msg": "Password has been reset"}, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class CreateMultipleUsers(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,  headers=headers)


class DeleteUserView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = DeleteSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            if email in settings.MANAGER:
                return Response({"msg": "This account cannot be deleted"}, status=status.HTTP_403_FORBIDDEN)
            try:
                user_to_delete = CustomUser.objects.get(email=email)

            except CustomUser.DoesNotExist as e:
                raise ValueError("This account does not exist")
            user_to_delete.delete()
            user = request.user
            email_send = user.email
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email_send, ]
            subject = 'Account Deleted'
            message = f'Hi {user.full_name}, your have successfully deleted this account - {email}.'
            send_mail(subject, message, email_from, recipient_list)
            return Response({"msg": f"Account with this email {email}  has been deleted"})
        return Response(serializer.errors)


class DeleteAllUsersView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    pass
