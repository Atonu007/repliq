from django.contrib.auth import authenticate
from .serializers import EmployeeSerializer, UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee
from django.shortcuts import get_object_or_404




# Generate Token Manually
def get_tokens_for_user(user):
    
    # Generate JWT tokens for a user.
   
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

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
    


