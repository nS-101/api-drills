from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    listed_on = models.DateField()
