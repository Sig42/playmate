from django.urls import path
from .views import SignUpView, ProfileUpdateView, ProfileDetailView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
]