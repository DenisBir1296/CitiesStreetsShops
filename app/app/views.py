import json

from django.db.models.fields import mixins
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework import viewsets

from . import models
from . import serializers


def data(request):
    if request.method == 'POST':
        req = request.body
        print('Результат : ', json.loads(req)['number'])
        return HttpResponse('ok')
    return HttpResponse('error')


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerialise

    @action(detail=True, methods=['get'])
    def street(self, request, pk):
        streets = models.Street.objects.filter(city_id=pk)
        data_ = serializers.StreetSerialise(streets, many=True).data
        return JsonResponse(data_, safe=False)


class ShopViewSet(viewsets.ModelViewSet):
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerialise

    def create(self, request, *args, **kwargs):

        return HttpResponse("ok_________")





