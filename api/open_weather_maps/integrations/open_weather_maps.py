from os import environ

import requests
from circuitbreaker import circuit
from requests.exceptions import ConnectionError
from rest_framework import status
from rest_framework.response import Response


class OpenWeatherMaps:
    API_URL = environ.get('OPENWEATHERMAPS_API_URL')
    API_KEY = environ.get('OPENWEATHERMAPS_API_KEY')
    BASE_QUERY = {'APPID': API_KEY, 'lang': 'pt_br', 'units': 'metric'}

    @circuit(failure_threshold=10, expected_exception=ConnectionError)
    def get_weather_of_city(self, city: str) -> (bool, Response or dict):
        response = requests.get(f'{self.API_URL}/weather', params={'q': city, **self.BASE_QUERY})
        status_code = response.status_code

        if status_code == status.HTTP_404_NOT_FOUND:
            return (
                False,
                {'data': {'mensagem': f'Cidade "{city}" não encontrada!'}, 'status': status.HTTP_404_NOT_FOUND},
            )
        elif status_code == status.HTTP_401_UNAUTHORIZED:
            return (
                False,
                {
                    'data': {'mensagem': 'Chave da API do Open Weather Maps invalida.'},
                    'status': status.HTTP_401_UNAUTHORIZED,
                },
            )
        return True, response.json()
