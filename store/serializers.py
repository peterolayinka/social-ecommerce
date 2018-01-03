from rest_framework import serializers

from account.serializers import UserSerializer
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta: 
        model = Store
        fields = ['owner', 'name', 'image', 'description']