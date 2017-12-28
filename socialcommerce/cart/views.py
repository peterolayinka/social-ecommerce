from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from store.models import Product, Order
from .cart import Cart
from .forms import CartAddProductForm, CartShippingDetail, UpdateOrderForm

# Create your views here.

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

@login_required
def cart_process(request):
    return render(request, 'cart/process.html', {})

class ProcessOrderView(generic.FormView):
    success_url = reverse_lazy('cart:user_orders')
    template_name = 'cart/process.html'
    form_class = CartShippingDetail

    def form_valid(self, form, **kwargs):
        # import pdb; pdb.set_trace()
        parent_form = super(ProcessOrderView, self).form_valid(form, **kwargs)
        cart = Cart(self.request)
        order = form.cleaned_data
        for item in cart:
            Order.objects.create(
                product=item['product'], user=self.request.user,
                store_id=item['store'], quantity=item['quantity'],
                price=item['price'], address=order['address'],
                city=order['city'], postal_code=order['postal_code'])
        messages.success(self.request, 'Order has been successfully placed.')
        # import pdb; pdb.set_trace()
        cart.clear()
        return parent_form

    def form_invalid(self, form):
        messages.success(self.request, 'Order could not be placed, An error occured.')

class OrderDetailView(generic.ListView):
    template_name = 'cart/orders.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.filter_order_based_on_query(self.request, user=self.request.user)

    def get_context_data(self):
        context = super(OrderDetailView, self).get_context_data()
        context['cancelled_order_count'] = Order.get_cancelled_order_count(self.request, user=self.request.user)
        context['awaiting_order_count'] = Order.get_awaiting_order_count(self.request, user=self.request.user)
        context['confirmed_order_count'] = Order.get_confirmed_order_count(self.request, user=self.request.user)
        context['total_order_count'] = Order.get_total_order_count(self.request, user=self.request.user)
        context['delivered_order_count'] = Order.get_delivered_order_count(self.request, user=self.request.user)
        context['processing_order_count'] = Order.get_processing_order_count(self.request, user=self.request.user)
        return context

@login_required
def update_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    form = UpdateOrderForm(instance=order)
    store =None
    if request.POST:
        form = UpdateOrderForm(instance=order, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            store = cd['store']
            form.save()
            messages.success(request, "Order successfully updated")
        else:
            messages.error(request, "Order update failed")

        if store =='True':
            return redirect(reverse_lazy('store:store_orders'))
        else:
            return redirect(reverse_lazy('cart:user_orders'))
