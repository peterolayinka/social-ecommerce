from rest_framework import serializers

from account.serializers import UserSerializer
from store.serializers import StoreSerializer
from .models import Message

class UnreadMessageSerializer(serializers.ModelSerializer):
    user_from = UserSerializer(read_only=True)
    user_to = UserSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['user_from', 'user_to', 'store', 'content', 'created']