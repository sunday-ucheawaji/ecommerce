from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from user_auth.serializers.user_serializers import (
    CustomUserSerializer)
from user_auth.models.custom_user import CustomUser
from datetime import datetime, timedelta
from user_auth.renderers import UserRenderers
# from rest_framework.renderers import BrowsableAPIRenderer

# Caching imports
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_cookie


class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserRenderers,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]  # view basis
    search_fields = ["first_name", "last_name", "user_type"]
    filterset_fields = ["first_name", "last_name", "user_type", "id"]
    ordering_fields = ["first_name", "last_name"]

    # Caching logic

    # @method_decorator(vary_on_cookie)
    # @method_decorator(cache_page(60*60))
    # def dispatch(self, *args, **kwargs):
    #     return super(UserListView, self).dispatch(*args, **kwargs)

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
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomerListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.filter(user_type="customer")
    serializer_class = CustomUserSerializer


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.filter(user_type="customer")
    serializer_class = CustomUserSerializer


class SupplierListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.filter(user_type="supplier")
    serializer_class = CustomUserSerializer


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.filter(user_type="supplier")
    serializer_class = CustomUserSerializer
