from django.urls import path
from . import views

# from store import

urlpatterns = [
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='single_product'),
]
