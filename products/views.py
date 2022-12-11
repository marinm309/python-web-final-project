from django.shortcuts import render, redirect
from django.views import generic as views
from .models import Products, Order, OrderItem
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from .forms import ShippingForm
from . utils import cart_details


MAIN_ORDER_CRITERIA = 'date_created'
PRODUCTS_PAGE_PAGINATION = 6
SINGLE_PRODUCT_SIMILAR_ITEAM_AMOUNT = 4

def home(request):
    categories = [x[0] for x in Products.CATEGORIES]
    print(categories)
    context = {
        'categories': categories
    }
    return render(request, 'products/home.html', context)


class ProductsListView(views.ListView):
    model = Products
    template_name = 'products/products.html'
    paginate_by = PRODUCTS_PAGE_PAGINATION

    def get_queryset(self):
        self.category = self.kwargs['category']
        queryset =  Products.objects.filter(category=self.category).order_by(MAIN_ORDER_CRITERIA)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Products.objects.filter(category=self.category).order_by(MAIN_ORDER_CRITERIA)
        total_results = products.count()
        context['category'] = self.category[0].upper() + self.category[1:]
        context['total_results'] = total_results
        context['pagination_number'] = self.paginate_by
        context['page_start_index'] = int(self.page_at) * self.paginate_by - self.paginate_by + 1
        context['page_end_index'] = int(self.page_at) * self.paginate_by if int(self.page_at) * self.paginate_by < total_results else total_results
        return context

    def get(self, request, *args, **kwargs):
        self.page_at = request.GET.get('page', 1)
        return super().get(request, *args, **kwargs)

class SingleProductView(views.ListView):
    model = Products
    template_name = 'products/single-product.html'

    def get_queryset(self):
        self.pk = self.kwargs['pk']
        self.category = self.kwargs['category']
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_queryset()
        product = Products.objects.get(pk=self.pk)
        same_cat_products = Products.objects.filter(category=self.category).order_by('?').exclude(pk=product.pk)
        context['product'] = product
        context['same_cat_products'] = same_cat_products[:SINGLE_PRODUCT_SIMILAR_ITEAM_AMOUNT]
        return context

def search(request):
    word = request.GET['search']
    page_at = int(request.GET.get('page', 1))
    object_list = Products.objects.filter(name__contains=word)
    p = Paginator(object_list, 6)
    page_obj = p.get_page(page_at)
    total_results = len(object_list)
    pagination_number = PRODUCTS_PAGE_PAGINATION
    page_start_index = int(page_at) * PRODUCTS_PAGE_PAGINATION - PRODUCTS_PAGE_PAGINATION + 1
    page_end_index = int(page_at) * PRODUCTS_PAGE_PAGINATION if int(page_at) * PRODUCTS_PAGE_PAGINATION < total_results else total_results
    context = {
        'object_list': object_list, 
        'total_results': total_results, 
        'pagination_number': pagination_number, 
        'page_start_index': page_start_index, 
        'page_end_index': page_end_index,
        'page_obj': page_obj,
        'word': word
    }
    return render(request, 'products/products.html', context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Products.objects.get(pk=product_id)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        order_item.quantity += 1
        amount_to_add = 1
    elif action == 'remove':
        order_item.quantity -= 1
        amount_to_add = -1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    total_cart_price = sum(map(lambda x :x.product.price * x.quantity, order.orderitem_set.all()))

    return JsonResponse({'total_cart_items': request.cart_items, 'amount_to_add': amount_to_add, 'total_cart_price': total_cart_price}, safe=False)

def delete_item(request, pk):
    customer = request.user.customer
    order = Order.objects.get(customer=customer)
    item = OrderItem.objects.get(pk=pk)
    item.delete()
    result = OrderItem.objects.filter(order=order).values()
    products_left = [entry for entry in result]

    return JsonResponse({'total_cart_items': request.cart_items, 'products_left': products_left}, safe=False)

def checkout(request):
    context_data = cart_details(request)
    items = context_data['items']
    total_items = context_data['total_items']
    total_price = context_data['total_price']
    order = context_data['order']
    customer = context_data['customer']

    if request.method == 'GET':
        form = ShippingForm()
    else:
        order.completed = True
        order.customer = None
        order.save()
        form = ShippingForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = customer
            address.order = order
            address.save()
            return redirect('home')
    context = {
        'items': items, 
        'total_items': total_items,
        'total_price': total_price,
        'form': form
    }
    return render(request, 'products/checkout.html', context)

def cart(request):
    context_data = cart_details(request)
    items = context_data['items']
    total_items = context_data['total_items']
    total_price = context_data['total_price']

    context = {
        'items': items,
        'total_items': total_items,
        'total_price': total_price
        }
    return render(request, 'products/cart.html', context)
