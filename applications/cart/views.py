from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from applications.cart.models import Order
from applications.cart.serializers import OrderSerializer


class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer): #скрыть какое нибудь окошко в postman
        serializer.save(customer=self.request.user)

