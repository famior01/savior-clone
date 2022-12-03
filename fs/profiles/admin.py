from django.contrib import admin
from .models import Profile, Relationship
# Register your models here.

@admin.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','user','email','bio', 'slug', 'created', 'update')

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
  list_display = ('id', 'sender', 'receiver', 'status', 'created', 'updated')