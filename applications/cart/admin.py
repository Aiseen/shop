from django.contrib import admin

# Register your models here.
from applications.cart.models import Order, CartItem, Cart

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)