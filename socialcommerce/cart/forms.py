from django import forms
from store.models import Order

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 101) ]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                            choices=PRODUCT_QUANTITY_CHOICES,
                            coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

class CartShippingDetail(forms.Form):
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    postal_code = forms.CharField(max_length=255)
    # address = forms.CharField(max_length=255)
    # city = forms.CharField

class UpdateOrderForm(forms.ModelForm):
    # status = forms.CharField(max_length=255)
    # cancellation_reason = forms.CharField(max_length=255)
    class Meta:
        model = Order
        fields = ['status', 'cancellation_reason']
