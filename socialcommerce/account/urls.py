from django.urls import path
from . import views

# from store import
app_name = 'account'

urlpatterns = [
    path('<slug:username>', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('edit/<slug:username>', views.edit_profile, name='edit_profile'),
]
