from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.decorators.http import require_POST
from django.views import generic
from django.contrib import messages

from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.

# class CartAddView(generic.FormView):
#     form_class = CartAddProductForm
#     success_url = '/cart'

#     def post(request):
#         self.cart = Cart(self.request)
#         self.product = get_object_or_404(Product, id=self.kwargs.get('id'))

#     def form_valid(request, form):
#         cd = form.cleaned_data
#         self.cart.add(product=self.product,
#                         quantity=cd['quantity'],
#                         update=cd['update'])

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                    quantity=cd['quantity'],
                    update_quantity=cd['update'])
        if cd['update'] == True:
            messages.success(
                request, f'<strong>{product.name}</strong> was successfully updated in cart.')
        else:
            messages.success(
                request, f'<strong>{product.name}</strong> was successfully added to cart.')
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product_id)
    messages.success(
        request, f'<strong>{product.name}</strong> was successfully removed from cart.')
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                            initial={'quantity': item['quantity'],
                                            'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
