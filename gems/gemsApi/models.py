from django.db import models



class HistoryDeals(models.Model):
    customer = models.TextField()
    item = models.TextField()
    total = models.FloatField()
    quantity = models.IntegerField()
    date = models.DateTimeField()
