from django import forms
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'about', 'address', 'city', 'telephone']
