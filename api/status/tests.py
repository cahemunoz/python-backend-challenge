from django.urls import reverse
from rest_framework import status

from status.apps import StatusConfig


class TestApp:
    def test_app_name(self):
        assert StatusConfig.name == 'status'


class TestView:
    def test_get_status(self, api_client):
        response = api_client.get(reverse('status'))

        assert {'OK': 'O serviço está funcionando!'} == response.json()
        assert response.status_code == status.HTTP_200_OK
