from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages

from .forms import UserForm, ProfileForm, UserRegistrationForm
from .models import Profile

User = get_user_model()

# Create your views here.

class ProfileDetailView(generic.DetailView):
    model = User
    template_name = 'account/profile.html'

    def get_object(self):
        # import pdb; pdb.set_trace()
        return get_object_or_404(User, username=self.kwargs.get('username'))

def edit_profile(request, username):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    if request.POST:
        user_form = UserForm(instance=request.user, data=request.POST)
        profile_form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            import pdb; pdb.set_trace()
            messages.success(request, "Profile could not be updated, An error occcured.")

    return render(request, 'account/edit_profile.html', {'user_form': user_form, 
                                                        'profile_form': profile_form})

def signup(request):
    user_form = UserRegistrationForm()
    if request.POST:
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = user_form.save(commit=False)
            user.set_password(cd['password'])
            user.save()
            user_auth = authenticate(username=cd['username'], password=cd['password'])
            login(request, user_auth)
            return redirect(reverse_lazy('index'))

    return render(request, 'registration/signup.html', {'user_form': user_form})
