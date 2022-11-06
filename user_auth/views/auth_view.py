from django.contrib.auth import authenticate
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from user_auth.serializers.user_serializers import CustomUserSerializer
from user_auth.serializers.auth_serializers import (
      LoginSerializer, LogoutSerializer, ResetPasswordSerializer, ChangePasswordSerializer, ForgotPasswordSerializer,RegisterSerializer, DeleteSerializer)
from user_auth.models.custom_user import CustomUser
from user_auth.jwt_authentication import JWTAuthentication
import random


class RegisterView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            full_name = serializer.data.get("full_name")
            email = request.data.get("email")
            subject = 'Welcome to Ecommerce world'
            message = f'Hi {full_name}, thank you for registering in ecommerce.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class LoginView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    auth_instance = JWTAuthentication()
    message = auth_instance.authenticate(request, True)
    return Response(message, status=status.HTTP_200_OK)


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
            raise ValueError("Email does not exist")
        otp =random.randint(1000,9999)
        check_otp_already_exist = CustomUser.objects.all().filter(otp=otp).exists()
        while check_otp_already_exist:
            otp =random.randint(1000,9999)
            check_otp_already_exist = CustomUser.objects.all().filter(otp=otp).exists()     
        user.otp=otp
        user.save()
        user_serialized= CustomUserSerializer(user)
        full_name = user_serialized.data.get("full_name")
        user_otp = user_serialized.data.get("otp")
        subject = 'OTP-Reset Password'
        message = f'Hi {full_name}, use this OTP-{user_otp} to reset password.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list)
        return Response({"OTP": f"Use this OTP-{user_otp} to reset password"})


class ChangePasswordView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes =(IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            print(user.check_password(old_password))
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({"msg": "Password changed successfully!"})
            return Response({"mesg": "Incorrect Password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)
            
            
class ResetPasswordView(APIView):
    authentication_classes = ()
    permission_classes =()
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            otp = serializer.data.get("otp")
            password = serializer.data.get("password")
            try:
                user = CustomUser.objects.get(otp=otp)
            except CustomUser.DoesNotExist as e:
                return Response({"msg":"Incorrect OTP"}, status=status.HTTP_400_BAD_REQUEST)
            if user.check_password(password):
                return Response({"This is an old Password! Set new password"})
            user.set_password(password)
            user.otp= 0
            user.save()
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

class DeleteUserView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes= ()
    serializer_class = DeleteSerializer

    def post(self, request):
        email = request.data["email"]        
        try:
            user_to_delete = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist as e:
            raise ValueError("This email does not exist")
        user_to_delete.delete()
        return Response({"msg": f"User with this {user_to_delete.get_full_name()} has been deleted"})

