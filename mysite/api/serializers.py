from .models import Coin, Job
from rest_framework import serializers


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "coins"]

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ["name", "price_change", "market_cap", "market_cap_rank", "volume", "volume_rank", "volume_change", "circulating_supply", "total_supply", "diluted_market_cap", "contracts", "official_links", "socials"]