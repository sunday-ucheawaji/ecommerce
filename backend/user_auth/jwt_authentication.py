import jwt
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from user_auth.models.custom_user import CustomUser
from user_auth.models.blacklist import BlackList
from rest_framework import exceptions
from django.conf import settings


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request, *args):
        is_logout = len(args) == 1

        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode("utf-8")
        auth_token = auth_data.split(" ")
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed("Token not valid")
        token = auth_token[1]

        if is_logout is True:
            BlackList.objects.create(token=token, custom_user=request.user)
            return {"message": "Logged Out !"}
        if is_logout is False:
            query_set = BlackList.objects.filter(token=token)
            if len(query_set) > 0:
                raise exceptions.AuthenticationFailed("Token is blacklisted")

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")
            email = payload["email"]
            user = CustomUser.objects.get(email=email)
            return (user, token)
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed(
                "Token is expired, login again")

        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed("Token is invalid")

        except CustomUser.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed("No such user")
