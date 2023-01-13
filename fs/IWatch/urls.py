from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IWatchListView, PostDeleteView, PostUpdateView,  IWatchDetailView, UploadVideoView, create_comment, like, dislike, SearchIWatch, TopWatchedView

app_name = 'IWatch'

urlpatterns = [
    path('', login_required(IWatchListView.as_view()), name='IWatch-main'),

    path('upload/', login_required(UploadVideoView.as_view()), name='upload-IWatch'),


    path('post/<int:pk>/delete/', login_required(PostDeleteView.as_view()), name='post-delete'),
    path('post/<int:pk>/update/', login_required(PostUpdateView.as_view()), name='post-update'),

    path('IWatch/<int:pk>/', login_required(IWatchDetailView.as_view()), name='Show-IWatch'),

    path('create_comment/', create_comment, name='create_comment'),
    path('like/', like, name='like'),
    path('dislike/', dislike, name='dislike'),
    path('search/', login_required(SearchIWatch.as_view()), name='search-IWatch'),
    path('top/', login_required(TopWatchedView.as_view()), name='top-IWatch'),


    

]
