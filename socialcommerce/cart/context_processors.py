from store.models import Product

from .cart import Cart
from .forms import CartAddProductForm

def cart(request):
    return {'cart': Cart(request),
            'cart_quantity_form': CartAddProductForm(),
            'sponsored_product': Product.objects.last()}

