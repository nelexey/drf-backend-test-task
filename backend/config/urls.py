from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/access/', include('apps.access_control.urls')),
    path('api/articles/', include('apps.articles.urls')),
]
