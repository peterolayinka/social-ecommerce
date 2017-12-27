from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user/%Y/%m/%d')
    about = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
