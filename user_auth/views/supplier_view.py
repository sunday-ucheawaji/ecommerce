from django.shortcuts import render
from rest_framework import generics, status
from user_auth.serializers.user_serializers import SupplierSerializer
from user_auth.models.supplier import Supplier


class SupplierListView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
