from django.shortcuts import render, redirect
from django.urls import reverse, path, include
from zakat_posts.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'crud', views.ZakatPostsViewSet, basename='zakat_posts')

urlpatterns = [
    path('', include(router.urls)),
]