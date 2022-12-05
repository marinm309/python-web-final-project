from django.shortcuts import render, redirect
from django.views import generic as views
from .models import Products

def home(request):
    return render(request, 'products/home.html')


class ProductsListView(views.ListView):
    model = Products
    template_name = 'products/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        return context

    def get_queryset(self):
        self.category = self.kwargs['category']
        products = Products.objects.filter(category=self.category).order_by('date_created')
        return  products