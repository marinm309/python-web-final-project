from django.views import generic as views
from . forms import CustomAuthenticationForm, SignUpForm, CustomerForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from products.models import ShippingAddress, Order, Products
from django.contrib.auth.decorators import login_required
from . models import Customer


UserModel = get_user_model()

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm


class UserCreationView(views.CreateView):
    template_name = 'users/register.html'
    form_class = SignUpForm
    success_url=reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    
class UserLogoutView(LogoutView):
    pass

@login_required(login_url='login')
def profile(request):
    user = request.user
    customer = user.customer
    address = ShippingAddress.objects.filter(customer=customer)
    orders = [x.order for x in address] if address else ''
    order_items = [x.orderitem_set.all() for x in orders] if orders else ''
    new_order_item = []
    for i in order_items:
        for j in i:
            new_order_item.append(j)
    print(new_order_item)
    products = {x.product for x in new_order_item} if order_items else ''
    context = {
        'customer': customer,
        'products': products
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    if request.method == 'GET':
        form = CustomerForm(instance=customer)
    else:
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)


@login_required(login_url='login')
def delete_profile(request):
    user = request.user
    customer = user.customer
    address = ShippingAddress.objects.filter(customer=customer)
    orders = [x.order for x in address] if address else ''
    order_items = [x.orderitem_set.all() for x in orders] if orders else ''
    products = [x.product for x in order_items[0]] if order_items else ''
    context = {
        'customer': customer,
        'products': products
    }
    return render(request, 'users/delete_profile.html', context)


@login_required(login_url='login')
def delete_profile_final(request):
    user = request.user
    customer = user.customer
    customer.delete()
    user.delete()
    return redirect('logout')