from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.cart.models import Order, CartItem
from applications.cart.serializers import OrderSerializer, CartItemSerializer


class CartItemView(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        # print(user.carts.first())
        queryset = queryset.filter(cart=user.carts.first())
        # return queryset[0:2]
        return queryset
class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer): #скрыть какое нибудь окошко в postman
        serializer.save(customer=self.request.user)

