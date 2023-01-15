from django.contrib import admin
from .models import ZakatPosts, ZakatPostsComment, UpVote, DownVote
# Register your models here.

# admin.site.register(ZakatPosts)
# admin.site.register(ZakatPostsComment)
# admin.site.register(UpVote)
# admin.site.register(DownVote)

@admin.register(ZakatPosts)
class ZakatPostsAdmin(admin.ModelAdmin):
    list_display = ('id','creator', 'seeker','phone_number', 'address', 'varified', 'paid', 'needed_money','satisfied', 'upvote', 'downvote', 'created', 'updated')
    
@admin.register(ZakatPostsComment)
class ZakatPostsCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'body', 'created_at', 'updated_at')

@admin.register(UpVote)
class UpVoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'post','upvoted', 'created', 'updated')

@admin.register(DownVote)
class DownVoteAdmin(admin.ModelAdmin):
    list_display = ('id','post','downvoted' ,'created', 'updated')
    