from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserProfileUpdateView,EmployeeCreateAPIView,EmployeeList
 
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile-update/', UserProfileUpdateView.as_view(), name='profile-update'),


    #employee
    path('create-employee/',EmployeeCreateAPIView.as_view(), name='create-employee'),   
    path('employees/', EmployeeList.as_view(), name='employee-list'),
  
]
    
  
