from django.urls import path
from .views import HistoryView, get_weather_data

urlpatterns = [
    path('weather/', get_weather_data, name='get_weather_data'),
    path('history/', HistoryView.as_view())
]