from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'