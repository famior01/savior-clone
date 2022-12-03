from django.contrib import admin
from .models import ZakatPosts, ZakatPostsComment, UpVote, DownVote
# Register your models here.

@admin.register(ZakatPosts)
class ZakatPostsAdmin(admin.ModelAdmin):
    list_display = ('creator', 'seeker', 'number1', 'spouse_name', 'number2', 'no_of_children', 'AI_varified', 'paid', 'expected_money', 'upvote', 'downvote', 'created', 'updated')
    
@admin.register(ZakatPostsComment)
class ZakatPostsCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'body', 'created_at', 'updated_at')

@admin.register(UpVote)
class UpVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'updated')

@admin.register(DownVote)
class DownVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'updated')