from decimal import Decimal
from django.conf import settings
from store.models import Product, Store

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart
        """

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 
                                     'price': str(product.price),
                                     'store': str(product.store.pk)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product_id):
        """
        Remove a product from cart.
        """
        product_id = str(product_id)
        # import pdb; pdb.set_trace()
        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """ Iterate throught the items in the cart and get the product instance """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            # item['store'] = Store.objects.get(pk=item['store'])
            yield item

    def __len__(self):
        """
        count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True