from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import JobSerializer, CoinSerializer
from .coinmarketcap import CoinMarketCap
from .models import Job, Coin
from .tasks import start_scraping_job

class StartScraping(APIView):
    def post(self, request):
        data = request.data
        coins = data["coins"]
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            start_scraping_job(job=serializer.instance, coins=coins)
        return Response(serializer.instance.id, status=status.HTTP_200_OK)

class GetCoinData(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            print(job_id)
            if not job.complete:
                data = {
                    "status": "Job Not Complete"
                }
                return Response(data)
            else:
                coins = Coin.objects.filter(job=job)
                coins_json = CoinSerializer(coins, many=True).data
                data = {
                    "job_id": job.id,
                    "tasks": coins_json
                }
                return Response(data)
        except Job.DoesNotExist:
            data = {
                "status": "Job Does not exist"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)