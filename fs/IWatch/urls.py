from django.urls import path
from .views import IWatchListView, like_unlike_post, PostDeleteView, PostUpdateView, post_of_following_profiles, IWatchDetailView, UploadVideoView

app_name = 'IWatch'

urlpatterns = [
    path('', IWatchListView.as_view(), name='IWatch-main'),

    path('upload/', UploadVideoView.as_view(), name='upload-IWatch'),


    path('like-post-view/', like_unlike_post, name='like-post-view'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

    path('IWatch/<int:pk>/', IWatchDetailView.as_view(), name='Show-IWatch')

]
