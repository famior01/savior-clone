from django.urls import path
from .views import IWatchListView, PostDeleteView, PostUpdateView,  IWatchDetailView, UploadVideoView, create_comment, like, dislike

app_name = 'IWatch'

urlpatterns = [
    path('', IWatchListView.as_view(), name='IWatch-main'),

    path('upload/', UploadVideoView.as_view(), name='upload-IWatch'),


    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

    path('IWatch/<int:pk>/', IWatchDetailView.as_view(), name='Show-IWatch'),

    path('create_comment/', create_comment, name='create_comment'),
    path('like/', like, name='like'),
    path('dislike/', dislike, name='dislike'),
    

]
