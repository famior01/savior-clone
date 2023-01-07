from django.contrib import admin
from .models import User

# Register your models here.

# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'full_name', 'email', 'religion', 'is_staff', 'is_active', 'date_joined', 'last_login')
