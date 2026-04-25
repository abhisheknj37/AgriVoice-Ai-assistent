from django.contrib import admin
from django.urls import path, include
from api.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('auth/', include('users.urls')),
    path('api/auth/', include('users.urls')),
    path('api/', include('api.urls')),
]
