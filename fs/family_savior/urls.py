import notifications.urls
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, notifications_read, notifications_delete, DeleteAllNotifications, ReadAllNotifications


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('IWatch/', include('IWatch.urls', namespace='IWatch')),
    path('zakat_posts/', include('zakat_posts.urls', namespace='zakat_posts')),
    path('user/', include('user.urls', namespace='user')),
    path('api/', include('zakat_posts.api.urls')),
    # for notifications
    re_path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('notifications_read/', notifications_read, name='notifications_read'),
    path('notifications_delete/<int:pk>/', notifications_delete, name='notifications_delete'),
    path('DeleteAllNotifications/', DeleteAllNotifications, name='DeleteAllNotifications'),
    path('ReadAllNotifications/', ReadAllNotifications, name='ReadAllNotifications'),
    re_path(r'hitcount/', include('hitcount.urls', namespace='hitcount')),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # for media files (user uploaded files)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # for static files (css, js, images)  
