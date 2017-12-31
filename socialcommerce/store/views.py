from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages 

from cart.forms import CartAddProductForm
from .models import Product, Order, Store, Category
from .forms import StoreForm, ProductForm
# Create your views here.

class IndexView(generic.ListView, generic.FormView):
    template_name = 'store/index.html'
    context_object_name = 'product_list'
    form_class = CartAddProductForm
    def get_queryset(self, **kwargs):
        # import pdb; pdb.set_trace()
        return Product.available_products.all().order_by('-created')

class ProductDetailView(generic.DetailView, generic.FormView):
    template_name = 'store/single_product.html'
    context_object_name = 'product'
    form_class = CartAddProductForm

    def get_object(self, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return product

@login_required
def store_orders(request):
    try:
        store = Store.objects.get(owner=request.user)
        orders = Order.filter_order_based_on_query(
            request, store=store)
    except:
        store = None
        orders = None

    context = {
        'store': store,
        'orders': orders,
        'cancelled_order_count': Order.get_cancelled_order_count(
                                                    request, store=store),
        'awaiting_order_count': Order.get_awaiting_order_count(
                                                    request, store=store),
        'confirmed_order_count': Order.get_confirmed_order_count(
                                                    request, store=store),
        'total_order_count': Order.get_total_order_count(
                                                    request, store=store),
        'delivered_order_count': Order.get_delivered_order_count(
                                                    request, store=store),
        'processing_order_count': Order.get_processing_order_count(
                                                    request, store=store),
    }
    return render(request, 'store/store_order_page.html', context)

@login_required
def store_create(request):
    store = request.user.store_owned
    if store:
        store_form = StoreForm(instance=store)
    else:
        store_form = StoreForm()
    # import pdb; pdb.set_trace()
    if request.POST:
        if store:
            store_form = StoreForm(instance=store, data=request.POST, files=request.FILES)
        else:
            store_form = StoreForm(request.POST, files=request.FILES)

        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.owner = request.user
            store.save()

        if not store:
            messages.success(request, 'Store successfully created')
            return redirect(reverse('store:store_orders'))

        messages.success(request, "Store successfully updated")
    return render(request, 'store/edit_store.html', {'store_form': store_form})

@login_required
def add_product(request, product_slug=None):
    categories = Category.objects.all()
    product = None
    if product_slug:
        product = get_object_or_404(Product, slug=product_slug)
        product_form = ProductForm(instance=product)
    else:
        product_form = ProductForm()

    if request.POST:
        if product_slug:
            product_form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        else:
            product_form = ProductForm(request.POST, files=request.FILES)

        if product_form.is_valid():
            product = product_form.save(request=request)
            if product_slug:
                messages.success(request,'Product successfully updated in store.')
            else:
                messages.success(request,'Product successfully added to store.')
        else:
            messages.error(request, 'An error occurred')
    return render(request, 'store/add_product.html', {
                                                    'product_form': product_form,
                                                    'categories': categories,
                                                    'product': product})

@login_required
def delete_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product.delete()
    messages.success(request, 'Product was successfully deleted')
    return redirect(reverse('store:view_products'))

@login_required
def view_products(request):
    product_list = Product.objects.filter(store=request.user.store_owned).order_by('-created')
    return render(request, 'store/store_product_list.html', {'product_list': product_list})

def search_store(request):
    return render(request, 'store/search.html', {})
