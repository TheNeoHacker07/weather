from django.http import JsonResponse
from rest_framework.generics import ListAPIView
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from .models import SearchHistory
from .serializer import HistorySerializer


cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_weather_data(request):
    
    latitude = request.GET.get('latitude', 52.52)
    longitude = request.GET.get('longitude', 13.41)
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m"
    }
    
    responses = openmeteo.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]

    
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ).tolist(),
        "temperature_2m": hourly_temperature_2m.tolist()
    }

    # Возврат данных в формате JSON
    return JsonResponse(hourly_data)


class HistoryView(ListAPIView):
    serializer_class = HistorySerializer

    def get_queryset(self):
        user = self.request.user
        return SearchHistory.objects.filter(user=user)
