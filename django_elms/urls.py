from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('discussions/', include('discussions.urls')),
    path('notifications/', include('notifications.urls')),
    path('certificates/', include('certificates.urls')),
    path('', include('django.contrib.auth.urls')),  # Django auth URLs (login, logout, etc.)
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)