from rest_framework import serializers
from .models import Employee, User,Device

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Adding password2 field for confirmation
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        # Define fields for registration serializer
        fields = ['email', 'name', 'password', 'password2', 'phone', 'address']
        extra_kwargs = {
            'password': {'write_only': True},  # Make password write-only
            'password2': {'write_only': True}  # Make password2 write-only
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        # Check if password matches password2
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        
        return attrs

    # Create user instance
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 from validated data
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)  # Field for email input

    class Meta:
        model = User
        fields = ['email', 'password']  # Fields required for login

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Define fields to be serialized in user profile
        fields = ['id', 'email', 'name', 'phone', 'address']




class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'department', 'user']
        read_only_fields = ['user']

    def create(self, validated_data):
        # Set the user field to the currently logged-in user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_user(self, value):
        
        #Ensure that the 'user' field matches the currently logged-in user.
      
        request = self.context.get('request')
        if value != request.user.id:
            raise serializers.ValidationError("You do not have permission to create an employee for this user.")
        return value

    def validate(self, data):
        
        #Validate the entire input data.
       
        # 'initial_data' contains the raw input data before validation.
        # It's not necessary to check 'initial_data' for the 'user' field here.
        if 'user' in self.initial_data:
            raise serializers.ValidationError("The 'user' field is not required as it is automatically derived from the logged-in user.")
        return data  
    

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'type', 'model', 'serial_number', 'purchase_date']

    def create(self, validated_data):
        return Device.objects.create(user=self.context['request'].user, **validated_data)
    