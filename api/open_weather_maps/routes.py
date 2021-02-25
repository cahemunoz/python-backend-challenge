from django.urls import path

from open_weather_maps.views import WeatherView


urlpatterns = [
    path('weather/<str:city>/', WeatherView.as_view(), name='weather')
]
