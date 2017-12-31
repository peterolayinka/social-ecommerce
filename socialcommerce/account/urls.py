from django.urls import path
from django.contrib.auth import views as auth_view

from . import views

# from store import
app_name = 'account'

urlpatterns = [
    path('<slug:username>', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('edit/<slug:username>', views.edit_profile, name='edit_profile'),
    path('login/', auth_view.login, name='login'),
    path('log-out/', auth_view.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    # path('change-password/', 'django.contrib.auth.login', name='change_password'),
    # path('/', 'django.contrib.auth.login', name='login')
]
