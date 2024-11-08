from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from .serializers import OrderSerializer
from .models import Order
# Create your views here.

# idk why i had to override this.
# Created custom pagination for only the page_size
# The page works out of the box.
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPageNumberPagination

    # Filter via ?status
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

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
