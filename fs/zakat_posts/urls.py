from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'zakat_posts'

urlpatterns = [
    path('', views.zakatPosts_comment_create_and_list_view, name='main-post-view'),
    path('upvote/', views.upvote, name='upvote'),
    path('downvote/', views.downvote, name='downvote'),
    path('delete/<int:pk>/', login_required(views.PostDeleteView.as_view()), name='post-delete'),
    path('update/<int:pk>/', login_required(views.PostUpdateView.as_view()), name='post-update'),
    path('satisfied/', views.satisfied, name='satisfied')
]   