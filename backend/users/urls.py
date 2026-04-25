from django.urls import path
from .views import register, login

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('users/', register),
    path('token/login/', login),
]
