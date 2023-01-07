from django.urls import path
from .views import post_comment_create_and_list_view, like_unlike_post, PostDeleteView, PostUpdateView, post_of_following_profiles

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='main-post-view'),
    path('like-post-view/', like_unlike_post, name='like-post-view'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

]
