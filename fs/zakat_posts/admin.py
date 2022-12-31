from django.contrib import admin
from .models import ZakatPosts, ZakatPostsComment, UpVote, DownVote
# Register your models here.

@admin.register(ZakatPosts)
class ZakatPostsAdmin(admin.ModelAdmin):
    list_display = ('id','creator','post_number', 'seeker', 'varified', 'paid', 'needed_money','satisfied', 'upvote', 'downvote', 'created', 'updated')
    
@admin.register(ZakatPostsComment)
class ZakatPostsCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'body', 'created_at', 'updated_at')

@admin.register(UpVote)
class UpVoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post','upvoted', 'created', 'updated')

@admin.register(DownVote)
class DownVoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post','downvoted' ,'created', 'updated')
    