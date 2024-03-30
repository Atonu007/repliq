from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Employee, User

class UserModelAdmin(BaseUserAdmin):
    # Displayed columns in the admin list view
    list_display = ('id', 'email', 'name', 'phone', 'address', 'is_admin')
    
    # Filter options on the right side in the admin
    list_filter = ('is_admin',)
    
    # Fieldsets for user details in the admin interface
    fieldsets = (
        ('User Credentials', {'fields': ('name', 'password')}),
        ('Personal info', {'fields': ('email', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    # Additional fields when adding a new user in the admin interface
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'address', 'password1', 'password2'),
        }),
    )
    
    # Search fields for searching users in the admin
    search_fields = ('email',)
    
    # Ordering of users in the admin interface
    ordering = ('name', 'id')
    
    # Fields displayed horizontally for the user in the admin interface
    filter_horizontal = ()

# Register the User model with the custom admin configuration
admin.site.register(User, UserModelAdmin)
admin.site.register(Employee)
