from django.db import models
from django.contrib.auth import get_user_model

from store.models import Store
# Create your models here.

User = get_user_model()

class MessageList(models.Model):
    user_from = models.ForeignKey(
        User, related_name='message_list_from', blank=True, null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='message_list_to_store',
                              on_delete=models.CASCADE, blank=True, null=True)
    user_to = models.ForeignKey(User, related_name='message_list_to_user',
                               on_delete=models.CASCADE, blank=True, null=True)
    user_from_read = models.BooleanField(default=False)
    store_read = models.BooleanField(default=False)
    user_to_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'message list from {self.user_from} to {self.user_to} {self.store}'

    class Meta:
        ordering = ('-created', 'user_from_read', 'user_to_read')


class Message(models.Model):
    user_from = models.ForeignKey(
        User, related_name="message_from", blank=True, null=True, on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        User, related_name='message_to', blank=True, null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(
        Store, related_name='store_to', blank=True, null=True, on_delete=models.CASCADE)
    from_store = models.BooleanField(default=False)
    content = models.TextField()
    message_list = models.ForeignKey(
        MessageList, related_name='message_list', on_delete=models.CASCADE)
    user_from_read = models.BooleanField(default=False)
    user_to_read = models.BooleanField(default=False)
    store_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'message item from {self.user_from} to {self.user_to} {self.store}'

    class Meta:
        ordering = ('created',)
