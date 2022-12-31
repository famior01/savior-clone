from django.contrib import admin
from .models import Profile, Relationship
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('id', 'first_name', 'last_name', 'user','post_no','bio', 'email', 'country', 'avatar', 'slug', 'created', 'updated')

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
  list_display = ('id', 'sender', 'receiver', 'status', 'created', 'updated')