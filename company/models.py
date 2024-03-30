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
        """
        Creates and saves a superuser with the given email, name, phone, address, and password.
        """
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
