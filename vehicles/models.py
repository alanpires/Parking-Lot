from django.db import models
from levels.models import Level


class Spot(models.Model):
    variety = models.CharField(max_length=255)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)


class Vehicle(models.Model):
    vehicle_type = models.CharField(max_length=255)
    license_plate = models.CharField(max_length=255)
    arrived_at = models.CharField(max_length=255, blank=True, null=True)
    paid_at = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.IntegerField(blank=True, null=True)
    spot = models.OneToOneField(Spot, on_delete=models.CASCADE)
