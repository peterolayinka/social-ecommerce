from django.contrib import admin
from django.forms import ModelForm
from django.contrib.gis.db import models

from mapwidgets.widgets import GooglePointFieldWidget

from .models import Store, Product, Category, Order
# from floppyforms.gis import PointWidget, BaseGMapWidget

# Register your models here.

# class CustomerPointWidget(PointWidget, BaseGMapWidget):
#     google_maps_api_key = ' AIzaSyAxsrulrQnEC1gRuZnOm1V1vROrIyOcx08'
#     class Media:
#         js = ('/static/floppyforms/js/MapWidget.js',)


# class ProductAdminForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'slug', 'category', 'image', 'description', 'processing_time', 'price', 'stock', 'available', 'location']
#         widgets = {
#             # 'location': CustomerPointWidget()
#         }

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    list_display = ['name', 'category', 'price', 'stock', 'available', 'location']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'store']
