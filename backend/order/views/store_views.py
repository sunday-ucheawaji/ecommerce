from rest_framework import generics
from order.models.store import Store
from order.serializers import StoreSerializer


class StoreListView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
