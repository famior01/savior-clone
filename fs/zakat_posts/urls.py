from django.urls import path
from .views import home

app_name = 'zakat_posts'

urlpatterns = [
    path('zakat_bat/', home, name='home'),
]