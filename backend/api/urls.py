from django.urls import path
from .views import ask, crops, forecast, predict, soil, history, predictions, conversation, home, profile, change_password

urlpatterns = [
    path('', home),
    path('predict/', predict),
    path('ask/', ask),
    path('crops/', crops),
    path('soil/', soil),
    path('forecast/', forecast),
    path('history/', history),
    path('predictions/', predictions),
    path('conversation/', conversation),
    path('profile/', profile),
    path('profile/change-password/', change_password),
]
