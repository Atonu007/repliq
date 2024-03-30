from rest_framework import serializers
from .models import User

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
