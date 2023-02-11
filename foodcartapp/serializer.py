from rest_framework.serializers import ModelSerializer
# from rest_framework.serializers import ListField

from .models import Order, OrderMenuItem


class OrderMenuItemSerializer(ModelSerializer):
    class Meta:
        model = OrderMenuItem
        fields = ['product', 'quantity']


class FoodcartappSerializer(ModelSerializer):
    products = OrderMenuItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']

