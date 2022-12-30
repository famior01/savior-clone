import notifications.urls
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('zakat_posts/', include('zakat_posts.urls', namespace='zakat_posts')),
    path('api/', include('zakat_posts.api.urls')),
    # for notifications
    re_path(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # for media files (user uploaded files)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # for static files (css, js, images) 
