from django.urls import path
from zakat_posts import views
from django.contrib.auth.decorators import login_required
app_name = 'zakat_posts'

urlpatterns = [
    path('', views.create_zakat_posts, name='main-post-view'),
    path('create_comment/', views.create_comment, name='create_comment'),
    path('upvote/', views.upvote, name='upvote'),
    path('downvote/', views.downvote, name='downvote'),
    path('delete/<int:pk>/', login_required(views.PostDeleteView.as_view()), name='post-delete'),
    path('update/<int:pk>/', login_required(views.PostUpdateView.as_view()), name='post-update'),
    path('satisfied/', views.satisfied, name='satisfied'),
    path('paid/', views.paid_money, name='paid'),
]   