from datetime import datetime
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

from open_weather_maps.models import City


class TestView:
    @pytest.fixture
    def city_name(self, fake):
        return fake.city()

    @pytest.fixture
    def city(self, city_name, db, fake, open_weather_maps_api_data):
        return City.objects.create(
            name=city_name,
            weather_description=(
                open_weather_maps_api_data['weather'][0]['description']
                if open_weather_maps_api_data.get('weather')
                else ''
            ),
            temp=open_weather_maps_api_data['main']['temp'],
            feels_like=open_weather_maps_api_data['main']['feels_like'],
            temp_min=open_weather_maps_api_data['main']['temp_min'],
            temp_max=open_weather_maps_api_data['main']['temp_max'],
            humidity=open_weather_maps_api_data['main']['humidity'],
        )

    @pytest.fixture
    def open_weather_maps_api_data(self, fake):
        return {
            'weather': [{'description': 'Nublado'}],
            'main': {
                'temp': fake.random_int(0, 40),
                'feels_like': fake.random_int(0, 40),
                'temp_min': fake.random_int(0, 20),
                'temp_max': fake.random_int(20, 40),
                'humidity': fake.random_int(0, 100),
            },
        }

    @pytest.fixture
    def expected_city(self, city_name, open_weather_maps_api_data):
        return {
            'name': city_name,
            'weather_description': open_weather_maps_api_data['weather'][0]['description'],
            'temp': open_weather_maps_api_data['main']['temp'],
            'feels_like': open_weather_maps_api_data['main']['feels_like'],
            'temp_min': open_weather_maps_api_data['main']['temp_min'],
            'temp_max': open_weather_maps_api_data['main']['temp_max'],
            'humidity': open_weather_maps_api_data['main']['humidity'],
        }

    @patch('open_weather_maps.views.OpenWeatherMaps.get_weather_of_city')
    def test_get_city_with_cache_into_time(
        self, mock_get_weather_of_city, api_client, city, city_name, expected_city, open_weather_maps_api_data
    ):
        city.created_at = datetime.min
        city.updated_at = datetime.min
        city.save()
        mock_get_weather_of_city.return_value = True, open_weather_maps_api_data

        response = api_client.get(reverse('weather', kwargs={'city': city_name}))

        assert response.data == expected_city
        assert response.status_code == status.HTTP_200_OK

    @patch('open_weather_maps.views.OpenWeatherMaps.get_weather_of_city')
    def test_get_city_with_cache_into_time_and_error_in_api(
        self, mock_get_weather_of_city, api_client, city, city_name, expected_city
    ):
        city.created_at = datetime.min
        city.updated_at = datetime.min
        city.save()
        mock_get_weather_of_city.return_value = (
            False,
            {'data': {'mensagem': 'Error interno!'}, 'status': status.HTTP_400_BAD_REQUEST},
        )

        response = api_client.get(reverse('weather', kwargs={'city': city_name}))

        assert response.data == {'mensagem': 'Error interno!'}
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('open_weather_maps.views.OpenWeatherMaps.get_weather_of_city')
    def test_get_city_with_out_cache(
        self, mock_get_weather_of_city, api_client, city_name, expected_city, db, open_weather_maps_api_data
    ):
        mock_get_weather_of_city.return_value = True, open_weather_maps_api_data

        response = api_client.get(reverse('weather', kwargs={'city': city_name}))

        assert response.data == expected_city
        assert response.status_code == status.HTTP_200_OK

    @patch('open_weather_maps.views.OpenWeatherMaps.get_weather_of_city')
    def test_get_city_with_out_cache_with_error_in_api(
        self, mock_get_weather_of_city, api_client, city_name, expected_city, db, open_weather_maps_api_data
    ):
        mock_get_weather_of_city.return_value = (
            False,
            {'data': {'mensagem': 'Error interno!'}, 'status': status.HTTP_400_BAD_REQUEST},
        )

        response = api_client.get(reverse('weather', kwargs={'city': city_name}))

        assert response.data == {'mensagem': 'Error interno!'}
        assert response.status_code == status.HTTP_400_BAD_REQUEST
