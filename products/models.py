from django.db import models
import uuid
from users.models import Customer


class Products(models.Model):
    CATEGORIES = (
        ('gaming', 'gaming'),
        ('toys', 'toys'),
        ('books', 'books'),
        ('music', 'music'),
        ('clothes', 'clothes'),
        ('pc_laptops', 'pc_laptops'),
        ('phones', 'phones'),
        ('tv_monitors', 'tv_monitors'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    producer = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=30, null=False, blank=False, choices=CATEGORIES)
    description = models.TextField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    img = models.ImageField(upload_to='products', null=False, blank=False)
    sub_img1 = models.ImageField(upload_to='products', null=True, blank=True)
    sub_img2 = models.ImageField(upload_to='products', null=True, blank=True)
    sub_img3 = models.ImageField(upload_to='products', null=True, blank=True)
    sub_img4 = models.ImageField(upload_to='products', null=True, blank=True)
    sub_img5 = models.ImageField(upload_to='products', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self) -> str:
        return str(self.id)

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Products, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)

class ShippingAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    zip = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address


class SlidingAdds(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='products')
