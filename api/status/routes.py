from django.urls import path
from status.views import ServiceStatus


urlpatterns = [
    path('about', ServiceStatus.as_view(), name='status')
]
