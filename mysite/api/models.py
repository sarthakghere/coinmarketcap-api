from django.db import models

# Create your models here.
class Job(models.Model):
    coins = models.JSONField()
    complete = models.BooleanField(null=True,default=False)

class Coin(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price = models.FloatField()
    price_change = models.FloatField()
    market_cap = models.FloatField()
    market_cap_rank = models.IntegerField()
    volume = models.FloatField()
    volume_rank = models.IntegerField()
    volume_change = models.FloatField()
    circulating_supply = models.FloatField()
    total_supply = models.FloatField()
    diluted_market_cap = models.FloatField()
    contracts = models.JSONField()
    official_links = models.JSONField()
    socials = models.JSONField()