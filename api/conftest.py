import pytest
from faker import Faker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def fake() -> Faker:
    return Faker('pt-BR')

