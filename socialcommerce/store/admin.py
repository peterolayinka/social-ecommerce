from django.contrib import admin
from .models import Store, Product, Category, Order

# Register your models here.

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'store']