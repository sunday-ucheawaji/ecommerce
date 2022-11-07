from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from user_auth.serializers.user_serializers import (
    CustomUserSerializer)
from user_auth.models.custom_user import CustomUser
from user_auth.models.blacklist import BlackList
from user_auth.jwt_authentication import JWTAuthentication
from datetime import datetime, timedelta


class UserListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]  # view basis
    search_fields = ["first_name", "last_name", "user_type"]
    filterset_fields = ["first_name", "last_name", "user_type", "id"]
    ordering_fields = ["first_name", "last_name"]

    """The search behavior may be restricted by prepending various characters to the search_fields.

    '^' Starts-with search.
    '=' Exact matches.
    '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    '$' Regex search."""

    # def get_queryset(self):
    #     query_set = CustomUser.objects.all()
    #     user_type = self.request.query_params.get("user_type")
    #     last_name = self.request.query_params.get("last_name")
    #     if user_type is not None and last_name is not None:
    #         return query_set.filter(Q(user_type=user_type) & Q(last_name=last_name))
    #     if user_type is not None and last_name is None:
    #         return query_set.filter(Q(user_type=user_type))
    #     if user_type is None and last_name is not None:
    #         return query_set.filter(Q(last_name=last_name))
    #     return query_set


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = ()
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    
