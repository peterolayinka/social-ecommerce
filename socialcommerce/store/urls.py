from django.urls import path
from . import views

# from store import

app_name="store"

urlpatterns = [
    path('create/', views.store_create, name='create_store'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='single_product'),
    path('orders/view/', views.store_orders, name='store_orders'),
    path('add/prodcut/', views.add_product, name='add_product'),
    path('edit/prodcut/<slug:product_slug>', views.add_product, name='edit_product'),
    path('delete/prodcut/<slug:product_slug>', views.delete_product, name='delete_product'),
    path('view/products/', views.view_products, name='view_products'),
    path('edit/store/', views.store_create, name='edit_store'),
]
