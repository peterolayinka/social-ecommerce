from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Product
from cart.forms import CartAddProductForm
# Create your views here.

class IndexView(generic.ListView, generic.FormView):
    template_name = 'store/index.html'
    context_object_name = 'product_list'
    form_class = CartAddProductForm

    def get_queryset(self, **kwargs):
        return Product.objects.all().order_by('-created')

class ProductDetailView(generic.DetailView, generic.FormView):
    template_name = 'store/single_product.html'
    context_object_name = 'product'
    form_class = CartAddProductForm

    def get_object(self, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return product

class CheckoutView():
    pass

class OrderView():
    pass

class ConfirmOrderView():
    pass

class CancelOrderView():
    pass

class AddStoreProductView():
    pass

class EditStoreProductView():
    pass

class ListStoreProductView():
    pass

class DeleteStoreProductView():
    pass

class CreateStoreView():
    pass

class EditStoreView():
    pass

class SearchView():
    pass
