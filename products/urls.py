from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', views.home, name='home'),
    path('products/search/', views.search, name='search'),
    path('products/<str:category>/', views.ProductsListView.as_view(), name='products'),
    path('products/<str:category>/<str:pk>/', views.SingleProductView.as_view(), name='single-product'),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.update_item, name='update-item'),
    path('delete_item/<str:pk>/', views.delete_item, name='delete-item'),
    path('checkout/', views.checkout, name='checkout'),
    path('create_product', views.create_product, name='create-product'),
    path('info', views.info, name='info'),
    path('orders_status', staff_member_required(views.OrdersStatusListView.as_view(), login_url='login'), name='orders-status'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete-order'),
]