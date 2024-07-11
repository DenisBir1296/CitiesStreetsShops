from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return str(self.name)


class Street(models.Model):
    name = models.CharField(max_length=30, null=False)
    city_id = models.ForeignKey('City', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return str(self.name)


class Shop(models.Model):
    name = models.CharField(max_length=30, null=False)
    street_id = models.ForeignKey('Street', on_delete=models.CASCADE)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return str(self.name)
