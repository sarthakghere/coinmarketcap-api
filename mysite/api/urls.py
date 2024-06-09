from django.urls import path
from . import views

urlpatterns = [
    path("api/taskmanager/start_scraping/",views.StartScraping.as_view()),
    path("api/taskmanager/scraping_status/<int:job_id>", views.GetCoinData.as_view())
]