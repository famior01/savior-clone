from django.contrib import admin
from .models import User

# Register your models here.

admin.site.register(User)

# @admin.register(User)
# class ZakatPostsAdmin(admin.ModelAdmin):
#     list_display = ('id','user','full_name', 'phone_number', 'religion', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions')