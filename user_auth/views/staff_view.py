from django.shortcuts import render
from rest_framework import generics, status
from user_auth.serializers.user_serializers import StaffSerializer
from user_auth.models.staff import Staff


class StaffListView(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
