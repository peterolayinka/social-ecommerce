from django.urls import path
from . import views

# from store import

app_name = "message"

urlpatterns = [
    path('', views.message_list, name='message_list'),
    path('message/<int:receipient_id>/<int:message_list>',
        views.single_message, name='single_message'),
    path('message/<int:receipient_id>/',
        views.single_message, name='start_chat'),
    path('send-message/<int:receipient_id>',
        views.send_message, name='send_message'),
    path('get-message/<int:receipient_id>',
        views.get_message, name='get_message'),
    # path('get_message/<int:receipient_id>/<int:message_list>', 
    #     views.message_list, name='message_list'),
]
