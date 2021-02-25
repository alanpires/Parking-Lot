from django.db import models

class Level(models.Model):
    name = models.CharField(max_length=255)
    fill_priority = models.IntegerField(blank=True, null=True)
    available_bike_spots = models.IntegerField(blank=True, null=True)
    available_car_spots = models.IntegerField(blank=True, null=True)