from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class ProfileDetailView(generic.DetailView):
    model = User
    template_name = ''

    def get_queryset(self):
        return User.objects.get(username=self.kwargs['username'])

class EditProfileView():
    pass

