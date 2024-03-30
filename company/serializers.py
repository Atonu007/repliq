from django.forms import ValidationError
from rest_framework import serializers
from .models import DeviceAssignment, Employee, User,Device,AssignmentLog

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
        fields = [ 'email', 'name', 'phone', 'address']




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
    


class DeviceAssignmentSerializer(serializers.ModelSerializer):
  assignment_history = serializers.SerializerMethodField()

  class Meta:
    model = DeviceAssignment
    fields = ['id', 'user', 'employee', 'device', 'checkout_date', 'checkout_note', 'return_date', 'return_note', 'assignment_history']
    read_only_fields = ['id', 'checkout_date', 'user', 'return_date', 'return_note', 'assignment_history']

  checkout_note = serializers.CharField(required=True)
  return_date = serializers.DateTimeField(required=True)
  employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=True)
  device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all(), required=True)

  def get_assignment_history(self, obj):
    assignments = DeviceAssignment.objects.filter(device=obj.device).order_by('-checkout_date')
    history = []
    for assignment in assignments:
      history.append({
          'employee_name': assignment.employee.name,
          'checkout_date': assignment.checkout_date,
          'checkout_note': assignment.checkout_note,
          'return_date': assignment.return_date,
          'return_note': assignment.return_note
      })
    return history

  def create(self, validated_data):
    # Extract user from request context
    user = self.context['request'].user

    # Retrieve additional required fields
    checkout_note = validated_data.pop('checkout_note')
    return_date = validated_data.pop('return_date')

    # Retrieve the employee instance
    employee_id = validated_data['employee'].id
    employee = Employee.objects.get(id=employee_id)

    # Check if employee belongs to the logged-in user (already exists in the code)

    # Check if device is already assigned (already exists in the code)

    # Create a new device assignment with user automatically set
    return DeviceAssignment.objects.create(
      user=user,
      employee=employee,
      device=validated_data['device'],
      checkout_note=checkout_note,
      return_date=return_date
    )
  




class AssignmentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentLog
        fields = '__all__'