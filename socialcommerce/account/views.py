from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class ProfileDetailView(generic.DetailView):
    model = User
    template_name = 'account/profile.html'

    def get_object(self):
        # import pdb; pdb.set_trace()
        return get_object_or_404(User, username=self.kwargs.get('username'))

class EditProfileView():
    pass

