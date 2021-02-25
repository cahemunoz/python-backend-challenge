from rest_framework.serializers import ModelSerializer

from open_weather_maps.models import City


class CitySerializer(ModelSerializer):
    class Meta:
        fields = ['name', 'weather_description', 'temp', 'feels_like', 'temp_min', 'temp_max', 'humidity']
        model = City
