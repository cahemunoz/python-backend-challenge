from datetime import datetime

from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import FloatField
from django.db.models import IntegerField
from django.db.models import Model


class City(Model):
    name = CharField(max_length=245, blank=False, null=False)
    weather_description = CharField(max_length=245)
    temp = FloatField()
    feels_like = FloatField()
    temp_min = FloatField()
    temp_max = FloatField()
    humidity = IntegerField()
    created_at = DateTimeField(default=datetime.utcnow, editable=False)
    updated_at = DateTimeField(default=datetime.utcnow)

    def check_cache_time(self):
        return divmod((datetime.utcnow() - self.updated_at).total_seconds(), 60)[0] >= 1

    def update_with_integration_open_weather_json_data(self, json: dict):
        self.updated_at = datetime.utcnow()
        self.weather_description = json['weather'][0]['description'] if json.get('weather') else ''
        self.temp = json['main']['temp']
        self.feels_like = json['main']['feels_like']
        self.temp_min = json['main']['temp_min']
        self.temp_max = json['main']['temp_max']
        self.humidity = json['main']['humidity']
        self.save()
