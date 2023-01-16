from django.contrib import admin
from .models import Profile
# Register your models here.


# admin.site.register(Profile)
# admin.site.register(Relationship)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('id','user','phone_number','cur_add','profession','post_no','picture', 'slogan','created', 'updated')
