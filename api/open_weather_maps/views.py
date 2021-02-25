from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from open_weather_maps.integrations.open_weather_maps import OpenWeatherMaps
from open_weather_maps.models import City
from open_weather_maps.serializers import CitySerializer


class WeatherView(GenericAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get(self, request, city):
        open_weather = OpenWeatherMaps()

        if city_obj := self.get_queryset().filter(name=city).first():
            if city_obj.check_cache_time():
                ok, city_json_or_response_data = open_weather.get_weather_of_city(city)
                if not ok:
                    return Response(**city_json_or_response_data)
                city_obj.update_with_integration_open_weather_json_data(city_json_or_response_data)
        else:
            ok, city_json_or_response_data = open_weather.get_weather_of_city(city)
            if not ok:
                return Response(**city_json_or_response_data)

            city_json = city_json_or_response_data
            city_obj = City.objects.create(
                name=city,
                weather_description=city_json['weather'][0]['description'] if city_json.get('weather') else '',
                temp=city_json['main']['temp'],
                feels_like=city_json['main']['feels_like'],
                temp_min=city_json['main']['temp_min'],
                temp_max=city_json['main']['temp_max'],
                humidity=city_json['main']['humidity'],
            )

        return Response(data=self.get_serializer(city_obj).data, status=status.HTTP_200_OK)
