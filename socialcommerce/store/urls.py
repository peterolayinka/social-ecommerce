from django.urls import path
from . import views
from message.views import message_list, single_message, send_message, get_message

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
    path('message/', message_list, name='store_messages'),
    path('send-message/<int:message_list_id>',
        send_message, name='store_send_message'),
    path('get-message/<int:message_list_id>',
        get_message, name='store_get_message'),
    path('message/<int:receipient_id>/<int:message_list>',
        single_message, name='single_message'),
    path('edit/store/', views.store_create, name='edit_store'),
]
