from rest_framework import generics
from .serializers import OrderSerializer
from .models import Order
# Create your views here.

class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save()

class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    Lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save()

class OrderDeleteAPIView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.delete()
