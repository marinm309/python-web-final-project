from django.shortcuts import render
from django.views import generic as views
from .models import Products

def home(request):
    return render(request, 'products/home.html')


class ProductsListView(views.ListView):
    model = Products
    template_name = 'products/products.html'
    paginate_by = 6

    def get_queryset(self):
        self.category = self.kwargs['category']
        queryset =  Products.objects.filter(category=self.category).order_by('date_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Products.objects.filter(category=self.category).order_by('date_created')
        total_results = products.count()
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
        context['same_cat_products'] = same_cat_products[:5]
        return context