from django.urls import path
from . import views

# from store import
app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('process/', views.ProcessOrderView.as_view(), name='cart_process'),
    path('orders/', views.OrderDetailView.as_view(), name='user_orders'),
    path('orders/update/<int:order_id>', views.update_order, name='update_order'),
    path('add/<int:product_id>', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),
]
