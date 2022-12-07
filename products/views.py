from django.shortcuts import render
from django.views import generic as views
from .models import Products

MAIN_ORDER_CRITERIA = 'date_created'
PRODUCTS_PAGE_PAGINATION = 6
SINGLE_PRODUCT_SIMILAR_ITEAM_AMOUNT = 4

def home(request):
    return render(request, 'products/home.html')


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
    word = request.POST['search']
    page_at = request.GET.get('page', 1)
    object_list = Products.objects.filter(name__contains=word)
    total_results = len(object_list)
    pagination_number = PRODUCTS_PAGE_PAGINATION
    page_start_index = int(page_at) * PRODUCTS_PAGE_PAGINATION - PRODUCTS_PAGE_PAGINATION + 1
    page_end_index = int(page_at) * PRODUCTS_PAGE_PAGINATION if int(page_at) * PRODUCTS_PAGE_PAGINATION < total_results else total_results
    context = {'object_list': object_list, 'total_results': total_results, 'pagination_number': pagination_number, 'page_start_index': page_start_index, 'page_end_index': page_end_index}
    return render(request, 'products/products.html', context)