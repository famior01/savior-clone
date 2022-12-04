from django.urls import path
from . import views

app_name = 'zakat_posts'

urlpatterns = [
    path('', views.zakatPosts_comment_create_and_list_view, name='main-post-view'),
    path('upvote/', views.upvote, name='upvote'),
    path('downvote/', views.downvote, name='downvote'),
]