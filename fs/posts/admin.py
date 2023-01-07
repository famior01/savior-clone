from django.contrib import admin
from .models import Posts, Comment, Like
# Register your models here.

# admin.site.register(Posts)
# admin.site.register(Comment)
# admin.site.register(Like)

@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','author', 'content', 'image', 'created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'post', 'body', 'created_at', 'updated_at')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'post', 'value', 'created_at', 'updated_at')
