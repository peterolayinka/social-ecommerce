import itertools

from django import forms
from django.utils.text import slugify

from .models import Store, Product, Category

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'image', 'address', 'city']

class ProductForm(forms.ModelForm):
    category = forms.CharField()
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'processing_time', 'price', 'available']

    def save(self, commit=True, **kwargs):
        if self.instance.pk:
            return super(ProductForm, self).save()
        instance = super(ProductForm, self).save(commit=False)
        cd = self.cleaned_data
        category = Category.objects.get(slug=cd['category'])
        instance.slug = orig = slugify(instance.name)
        instance.user = kwargs['request'].user
        instance.store = kwargs['request'].user.store_owned
        instance.category = category

        for x in itertools.count(1):
            if not Product.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = f'{orig}-{x}'
        instance.save()
        return instance
