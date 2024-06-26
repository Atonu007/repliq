from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, address, password=None):
       
        #Creates and saves a User with the given email, name, phone, address, and password.
       
        if not email:
            raise ValueError('User must have an email address')

        # Normalize the email address to lowercase
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            address=address,
        )

        # Set the password (if provided) and save the user
        user.set_password(password)
        user.save(using=self._db)
        return user
   
    def create_superuser(self, email, name, phone, address, password=None):
        # Createing and saves a superuser with the given email, name, phone, address, and password.
        # Call create_user method to create a user
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone,
            address=address,
        )
        
        # Set the user as admin and save
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)  
    address = models.CharField(max_length=255)  
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()  # Use UserManager for managing users

    USERNAME_FIELD = 'email'  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = ['name', 'phone', 'address']  # Fields required when creating a user

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
       
        # Simplest possible answer: Yes, always for admin
        return self.is_admin

    def has_module_perms(self, app_label):
       
        # Simplest possible answer: Yes, always for admin
        return True

    @property
    def is_staff(self):
       
        # Simplest possible answer: All admins are staff
        return self.is_admin




# Createing Employee Model.
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name =models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Createing Employee Model.
class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)  
    purchase_date = models.DateField()

    def __str__(self):
        return self.model
    

#creating decive assignment model
class DeviceAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    checkout_note = models.TextField()
    return_date = models.DateTimeField(null=True, blank=True)
    return_note = models.TextField(null=True, blank=True)
    def return_device(self, return_date, return_note):
        # Implement logic to handle device return (e.g., update status, send notifications)
        self.is_returned = True  
        self.save()

#creting the log to track the device assginment history
class AssignmentLog(models.Model):
    assignment = models.ForeignKey(DeviceAssignment, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)

    checkout_date = models.DateTimeField()
    checkout_note = models.TextField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    return_note = models.TextField(blank=True, null=True)


   