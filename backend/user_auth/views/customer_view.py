from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from user_auth.serializers import CustomerSerializer
from user_auth.models.customer import Customer


class RegisterCustomerView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     customers = Customer.objects.all()
    #     serializer = self.serializer_class(customers, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
