# from django.contrib import admin
# from .models import User

# # Register your models here.

# # admin.site.register(User)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id','username', 'full_name', 'email', 'religion', 'is_staff', 'is_active', 'date_joined', 'last_login')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User


class FSUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('id','email', 'username','full_name','religion','gender','is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('email', 'username','is_staff', 'is_active',)
    fieldsets = (
        ('FS_USERS_INFO', {'fields': ('email',  'username', 'full_name', 'religion','password','gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        ('Add New FS', {
            'classes': ('wide',),
            'fields': ('email','username', 'full_name','religion', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','username', 'religion', 'gender')
    ordering = ('email','username', 'religion', 'gender')


admin.site.register(User, FSUserAdmin)