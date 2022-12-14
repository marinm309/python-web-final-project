from django.shortcuts import render, redirect
from django.views import generic as views
from .models import Products, Order, OrderItem, ShippingAddress, SlidingAdds, SmallAds
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from .forms import ShippingForm, ProductForm
from . utils import cart_details
from users.models import Customer
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required

UserModel = get_user_model()
MAIN_ORDER_CRITERIA = 'date_created'
PRODUCTS_PAGE_PAGINATION = 8
SINGLE_PRODUCT_SIMILAR_ITEAM_AMOUNT = 4

def home(request):
    sliding_ads = SlidingAdds.objects.all()
    categories = [x[0] for x in Products.CATEGORIES]
    small_ads = SmallAds.objects.all()
    context = {
        'categories': categories,
        'sliding_ads': sliding_ads,
        'small_ads': small_ads
    }
    return render(request, 'products/home.html', context)


class ProductsListView(views.ListView):
    model = Products
    template_name = 'products/products.html'
    paginate_by = PRODUCTS_PAGE_PAGINATION

    def get_queryset(self):
        self.category = self.kwargs['category']
        if self.category == 'newest':
            queryset = Products.objects.all().order_by(MAIN_ORDER_CRITERIA)
        elif self.category == 'hot':
            order_items = OrderItem.objects.all().order_by('product')
            order_items_count_dict = {}
            for i in order_items:
                product_name = i.product.name
                if product_name not in order_items_count_dict.keys():
                    order_items_count_dict[product_name] = 0
                order_items_count_dict[product_name] += i.quantity
            order_items_count_dict = dict(sorted(order_items_count_dict.items(), key=lambda item: -item[1]))
            order_items_lst = order_items_count_dict.keys()
            queryset = Products.objects.filter(name__in=order_items_lst)
        else:
            queryset =  Products.objects.filter(category=self.category).order_by(MAIN_ORDER_CRITERIA)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.category == 'newest':
            products = Products.objects.all().order_by(MAIN_ORDER_CRITERIA)
        elif self.category == 'hot':
            products = self.get_queryset()
        else:
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
        product = Products.objects.get(pk=self.pk)
        same_cat_products = Products.objects.filter(category=self.category).order_by('?').exclude(pk=product.pk)
        context['product'] = product
        context['same_cat_products'] = same_cat_products[:SINGLE_PRODUCT_SIMILAR_ITEAM_AMOUNT]
        return context

def search(request):
    word = request.GET['search']
    page_at = int(request.GET.get('page', 1))
    object_list = Products.objects.filter(name__icontains=word)
    p = Paginator(object_list, PRODUCTS_PAGE_PAGINATION)
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
    product = Products.objects.get(pk=pk)
    item = OrderItem.objects.get(product=product, order=order)
    item.delete()
    result = OrderItem.objects.filter(order=order).values()
    products_left = [entry for entry in result]

    return JsonResponse({'total_cart_items': request.cart_items, 'products_left': products_left}, safe=False)

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


def checkout(request):
    context_data = cart_details(request)
    items = context_data['items']
    total_items = context_data['total_items']
    if total_items == 0:
        return redirect('home')
    total_price = context_data['total_price']
    order = context_data['order']
    customer = context_data['customer']

    if request.method == 'GET':
        if request.user.is_authenticated:
            form = ShippingForm(initial={'name': f'{customer.name}', 'email': f'{customer.user.email}'})
        else:
            form = ShippingForm()
    else:
        if request.user.is_authenticated:
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
        else:
            form = ShippingForm(request.POST)
            name = request.POST['name']
            email = request.POST['email']
            user, user_created = UserModel.objects.get_or_create(email=email)
            customer, customer_created = Customer.objects.get_or_create(user=user)
            customer.name = name
            customer.save()
            if form.is_valid():
                order = Order.objects.create(completed=True)
                address = form.save(commit=False)
                address.customer = customer
                address.order = order
                address.save()
                for item in items:
                    product = Products.objects.get(pk=item['product']['id'])
                    OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])
                response = redirect('home')
                response.delete_cookie('cart')
                return response

    context = {
        'items': items, 
        'total_items': total_items,
        'total_price': total_price,
        'form': form
    }
    return render(request, 'products/checkout.html', context)


@staff_member_required(login_url='login')
def create_product(request):
    if request.method == 'GET':
        form = ProductForm()
    else:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'products/create_product.html', context)

def info(request):
    return render(request, 'products/info.html')

class OrdersStatusListView(views.ListView):
    model = ShippingAddress
    template_name = 'products/orders_status.html'

@staff_member_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    address = ShippingAddress.objects.get(order=order)
    order.delete()
    address.delete()
    return redirect('orders-status')
