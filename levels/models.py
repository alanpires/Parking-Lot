from django.db import models


class Spot(models.Model):
    available_bike_spots = models.IntegerField()
    available_car_spots = models.IntegerField()


class Level(models.Model):
    name = models.CharField(max_length=255)
    fill_priority = models.IntegerField(blank=True, null=True)
    available_spots = models.ForeignKey(Spot, on_delete=models.CASCADE, blank=True, null=True)
    