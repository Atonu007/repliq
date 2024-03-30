from django.urls import path
from .views import MarkDeviceReturned,AddDevice, DeviceAssignmentView, DeviceDeleteAPIView, DeviceDetail, DeviceUpdateAPIView, AllDevices, UserRegistrationView,UserLoginView,UserProfileView,UserProfileUpdateView,EmployeeCreateAPIView,EmployeeList,Employeee,EmployeeUpdateAPIView, EmployeeDeleteAPIView
 
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
    path('device-detail/<int:id>/', DeviceDetail.as_view(), name='device-detail'),
    path('devices-update/<int:id>/', DeviceUpdateAPIView.as_view(), name='update_device'),
    path('devices-del/<int:id>/', DeviceDeleteAPIView.as_view(), name='delete_device'),


    #Device Assignment
    path('device-assignments/', DeviceAssignmentView.as_view(), name='device-assignments'),
    path('device-return/', MarkDeviceReturned.as_view(), name='device-return')

  
]
    
  
