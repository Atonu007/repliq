from django.urls import path
from .views import  UserLoginView, UserProfileUpdateView, UserProfileView, UserRegistrationView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile-update/', UserProfileUpdateView.as_view(), name='profile-update'),
    
  
]