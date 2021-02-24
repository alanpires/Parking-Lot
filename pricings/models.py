from django.db import models


class Pricing(models.Model):
    a_coefficient = models.IntegerField()
    b_coefficient = models.IntegerField()