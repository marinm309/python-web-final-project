from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<str:category>/', views.ProductsListView.as_view(), name='products'),
    path('products/<str:category>/<str:pk>/', views.SingleProductView.as_view(), name='single-product'),
    path('products/search/<str:keyword>/', views.search, name='search'),
]