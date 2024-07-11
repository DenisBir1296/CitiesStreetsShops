from django.http import HttpResponse
from rest_framework import serializers
from . import models


class CitySerialise(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class StreetSerialise(serializers.ModelSerializer):
    class Meta:
        model = models.Street
        fields = ['id', 'name']


class ShopSerialise(serializers.ModelSerializer):
    street_name = serializers.CharField(source='street_id')
    city_name = serializers.CharField(source='street_id.city_id')

    class Meta:
        model = models.Shop
        fields = ['id', 'name', 'street_name', 'city_name', 'open_time', 'close_time']
