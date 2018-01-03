from django.contrib import admin
from .models import MessageList, Message

# Register your models here.

@admin.register(MessageList)
class MessageListAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ['user_to', 'user_from', 'store']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    class Meta:
        model = Message
        list_display = ['user_to', 'user_from', 'store']
