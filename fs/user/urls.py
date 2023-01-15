from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'user'


urlpatterns = [
    path('update/<int:pk>/', login_required(views.UserUpdateView.as_view()), name='user-update'),
]