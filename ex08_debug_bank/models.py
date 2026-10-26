from django.db import models


class Account(models.Model):
    owner = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)  # in pence
    frozen = models.BooleanField(default=False)
