from django.db import models


class Loan(models.Model):
    book_title = models.CharField(max_length=200)
    member = models.CharField(max_length=100)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
