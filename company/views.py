from django.utils import timezone
from django.contrib.auth import authenticate
from .serializers import AssignmentLogSerializer, DeviceAssignmentSerializer, DeviceSerializer, EmployeeSerializer, UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import AssignmentLog, Device, Employee,DeviceAssignment
from django.shortcuts import get_object_or_404




# Generate Token Manually
def get_tokens_for_user(user):
    
    # Generate JWT tokens for a user.
   
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#user related views
class UserRegistrationView(APIView):
   
    #API endpoint for user registration.
   
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Registration Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    
    # API endpoint for user login.
    
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            
            user = authenticate(email=email, password=password)
            
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  
    #API endpoint for retrieving user profile.
   
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Serialize user profile
        user_profile_serializer = UserProfileSerializer(request.user)

        # Prepare response data
        response_data = {
            'user_profile': user_profile_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

class UserProfileUpdateView(APIView):
   
    # API endpoint for updating user profile.
   
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        # Get the logged-in user
        user = request.user
        
        # Deserialize the request data
        serializer = UserProfileSerializer(instance=user, data=request.data, partial=True)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the updated profile data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If the data is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#Employee related views
class EmployeeCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Create a serializer instance with request data and context
        serializer = EmployeeSerializer(data=request.data, context={'request': request})
        
        # Check if serializer is valid
        if serializer.is_valid():
            # Save the serializer data
            serializer.save()
            # Return the serialized data with 201 status code if successful
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return serializer errors with 400 status code if not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeList(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        # Filter employees based on the logged-in user
        employees = Employee.objects.filter(user=request.user)
        # Serialize the filtered queryset
        serializer = EmployeeSerializer(employees, many=True)
        # Return serialized data
        return Response(serializer.data)
    


class Employeee(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request,id):
        
        employee = Employee.objects.get(id=id)  
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
class EmployeeUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, format=None):
        try:
            employee = Employee.objects.get(id=id, user=request.user)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmployeeDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, format=None):
        # Get the employee object or return 404 if not found
        employee = get_object_or_404(Employee, id=id)
        
        # Check if the employee belongs to the requesting user
        if employee.user != request.user:
            return Response({"detail": "You are not authorized to delete this employee."}, status=status.HTTP_403_FORBIDDEN)
        
        # Delete the employee
        employee.delete()
        
        # Return success response
        return Response({"detail": "Employee deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    



#Device related view
class AddDevice(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Create a new device with the provided data
        serializer = DeviceSerializer(data=request.data, context={'request': request})
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the device
            serializer.save()
            # Return success response with created device data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return error response with serializer errors if data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllDevices(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Get all devices belonging to the requesting user
        devices = Device.objects.filter(user=request.user)
        # Serialize the devices
        serializer = DeviceSerializer(devices, many=True)
        # Return serialized data
        return Response(serializer.data)

class DeviceDetail(APIView):
    permission_classes =[IsAuthenticated]

    def get(self, request, id):
        # Get the device by id or return 404 if not found
        device = get_object_or_404(Device, id=id)
        # Serialize the device
        serializer = DeviceSerializer(device)
        # Return serialized device data
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeviceUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, format=None):
        # Get the device object or return 404 if not found
        device = get_object_or_404(Device, id=id)
        
        # Check if the device belongs to the requesting user
        if device.user != request.user:
            # Return forbidden response if the device does not belong to the user
            return Response({"detail": "You are not authorized to update this device."}, status=status.HTTP_403_FORBIDDEN)
        
        # Update the device with the provided data
        serializer = DeviceSerializer(device, data=request.data, context={'request': request})
        # Check if the data is valid
        if serializer.is_valid():
            # Save the updated device
            serializer.save()
            # Return success response with updated device data
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Return error response with serializer errors if data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, format=None):
        # Get the device object or return 404 if not found
        device = get_object_or_404(Device, id=id)
        
        # Check if the device belongs to the requesting user
        if device.user != request.user:
            # Return forbidden response if the device does not belong to the user
            return Response({"detail": "You are not authorized to delete this device."}, status=status.HTTP_403_FORBIDDEN)
        
        # Delete the device
        device.delete()
        
        # Return success response
        return Response({"detail": "Device deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    



class DeviceAssignmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeviceAssignmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class MarkDeviceReturned(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        assignment_id = request.data.get('assignment_id')
        return_note = request.data.get('return_note')

        
        if not return_note:
            return Response({"error": "Return note is required."}, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            assignment = DeviceAssignment.objects.get(id=assignment_id)
        except DeviceAssignment.DoesNotExist:
            return Response({"error": "Device assignment not found."}, status=status.HTTP_404_NOT_FOUND)

       
        assignment.return_date = timezone.now()  

     

        
        assignment.return_device(return_date=assignment.return_date, return_note=return_note)

       
        assignment_log_data = {
            'assignment': assignment.id,
            'assigned_to': assignment.employee.user.id,
            'checkout_date': assignment.checkout_date,
            'checkout_note': assignment.checkout_note,
            'return_date': assignment.return_date,
            'return_note': return_note
        }

      

        assignment_log_serializer = AssignmentLogSerializer(data=assignment_log_data)

        if assignment_log_serializer.is_valid():
            assignment_log_serializer.save()  
        else:
            return Response(assignment_log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

        return Response({"message": "Device marked as returned successfully."}, status=status.HTTP_200_OK)
    


class DeviceLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = AssignmentLog.objects.all()
        serializer = AssignmentLogSerializer(logs, many=True)
        return Response(serializer.data)
    


class DeviceLogDetailView(APIView):
    def get(self, request, device_id):
        try:
            log = AssignmentLog.objects.get(pk=device_id)
        except AssignmentLog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AssignmentLogSerializer(log)
        return Response(serializer.data)