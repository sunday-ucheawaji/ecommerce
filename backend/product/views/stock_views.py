from rest_framework import generics
from product.models.category import Stock
from product.serializers import StockSerializer


class StockListView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
