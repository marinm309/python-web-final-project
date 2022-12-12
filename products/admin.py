from django.contrib import admin
from . models import Products, Order, OrderItem, ShippingAddress

# admin.site.register(Products)
# admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)

@admin.register(Order, OrderItem, Products, ShippingAddress)
class OrderInfoAdmin(admin.ModelAdmin):
    pass

