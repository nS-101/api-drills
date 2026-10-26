from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    venue = models.CharField(max_length=100)
    date = models.DateField()
    capacity = models.IntegerField()
    booked = models.IntegerField(default=0)
