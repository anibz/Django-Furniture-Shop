from django.urls import path
from .views import (
    UserRegistrationView,
    user_login,
    user_profile,
    user_profile_update,
    change_password
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', user_login, name='login'),
    path('profile/', user_profile, name='profile'),
    path('profile/update/', user_profile_update, name='profile-update'),
    path('change-password/', change_password, name='change-password'),
]