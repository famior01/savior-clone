from django.contrib import admin
from .models import IWatch, IWatchComment, Like, Dislike, IWatchIncome


@admin.register(IWatch)
class IWatchAdmin(admin.ModelAdmin):
    list_display = ('id','creator', 'title', 'video','liked', 'disliked', 'created')
      

@admin.register(IWatchComment)
class IWatchCommentAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'IWatch', 'body', 'created')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'IWatch', 'liked', 'created')

@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'IWatch', 'disliked', 'created')


@admin.register(IWatchIncome)
class IWatchIncomeAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'IWatch', 'amount', 'created')