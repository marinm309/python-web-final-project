from django.contrib import admin
from . models import Products, Order, OrderItem, ShippingAddress


@admin.register(Order)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'completed')
    list_filter = ('completed', )
    ordering = ('-completed', )

@admin.register(Products)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'producer')
    list_filter = ('category', 'producer')

@admin.register(OrderItem)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'order')
    list_filter = ('order', )

@admin.register(ShippingAddress)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('customer', 'country', 'city', 'zip', 'address')
    list_filter = ('order', )

