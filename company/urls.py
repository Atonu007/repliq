from django.urls import path
from .views import AddDevice, AllDevices, UserRegistrationView,UserLoginView,UserProfileView,UserProfileUpdateView,EmployeeCreateAPIView,EmployeeList,Employeee,EmployeeUpdateAPIView, EmployeeDeleteAPIView
 
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile-update/', UserProfileUpdateView.as_view(), name='profile-update'),


    #employee
    path('create-employee/',EmployeeCreateAPIView.as_view(), name='create-employee'),   
    path('employees/', EmployeeList.as_view(), name='employee-list'),
    path('employee/<int:id>/', Employeee.as_view(), name='employe-detail'),
    path('employee-update/<int:id>/',EmployeeUpdateAPIView.as_view(), name='employe-update'),
    path('employees-delete/<int:id>/', EmployeeDeleteAPIView.as_view(), name='delete_employee'),


    #Device
    path('devices-create/', AddDevice.as_view(), name='device-create'),
    path('devices/', AllDevices.as_view(), name='device-list'),
   

  
]
    
  
