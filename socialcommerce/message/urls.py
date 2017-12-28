from django.urls import path
from . import views

# from store import

app_name = "message"

urlpatterns = [
    path('', views.message_list, name='message_list'),
]
