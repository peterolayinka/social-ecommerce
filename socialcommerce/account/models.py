from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from store.models import Category

# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user/%Y/%m/%d', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    interests = models.ManyToManyField(Category, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.user}\'s profile'

