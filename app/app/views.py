import json

from django.db import models
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from django.db.utils import DatabaseError
from django.db.models import Q
from django.utils import timezone

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


class ShopViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerialise

    def list(self, request, *args, **kwargs):
        city_name = request.GET.get('city', None)
        street_name = request.GET.get('street', None)
        is_open = request.GET.get('open', None)

        if city_name is not None:
            city_id = models.City.objects.filter(name=city_name).values_list('id')
            if not len(city_id):
                return JsonResponse({}, status=200)

        if street_name is None:
            if city_name is not None:
                street_id = models.Street.objects.filter(city_id__in=city_id).values_list('id')
        else:
            if city_name is None:
                street_id = models.Street.objects.filter(name=street_name).values_list('id')
            else:
                street_id = models.Street.objects.filter(city_id__in=city_id, name=street_name).values_list('id')

        if (city_name is None) and (street_name is None):
            shops = models.Shop.objects.all()
        else:
            if not len(street_id):
                return JsonResponse({}, status=200)
            shops = models.Shop.objects.all().filter(street_id__in=street_id)

        if is_open is not None:
            now = timezone.localtime()
            if str(is_open) == '0':
                shops = shops.filter(Q(open_time__gt=now) | Q(close_time__lt=now))
            else:
                shops = shops.filter(open_time__lt=now, close_time__gt=now)

        data_ = serializers.ShopSerialise(shops, many=True).data

        return JsonResponse(data_, status=200, safe=False)

    def create(self, request, *args, **kwargs):
        try:
            shop_name = request.data['name']
            street_name = request.data['street_name']
            city_name = request.data['city_name']
            close_time = request.data['close_time']
            open_time = request.data['open_time']
        except KeyError as e:
            return JsonResponse({str(e): ["This field is required."]}, status=400)

        city, city_created = models.City.objects.get_or_create(name=city_name)
        street, street_created = models.Street.objects.get_or_create(name=street_name, city_id=city)

        try:
            shop = models.Shop.objects.create(name=shop_name, open_time=open_time,
                                              close_time=close_time, street_id=street)
        except DatabaseError:
            if city_created:
                city.delete()
            if street_created:
                street.delete()

            return JsonResponse({'Error': 'Shop exist'}, status=400)

        return JsonResponse(serializers.ShopSerialise(shop).data, safe=False, status=201)

    def destroy(self, request, *args, **kwargs):
        try:
            shop = models.Shop.objects.get(id=kwargs['pk'])
            street_id = shop.street_id.id
            shop.delete()
        except models.Shop.DoesNotExist:
            return JsonResponse({}, status=404)

        if not models.Shop.objects.filter(street_id=street_id).exists():
            street = models.Street.objects.get(id=street_id)
            city_id = street.city_id.id
            street.delete()

            if not models.Street.objects.filter(city_id=city_id).exists():
                models.City.objects.get(id=city_id).delete()

        return JsonResponse({}, status=204)
