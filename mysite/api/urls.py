from django.urls import path
from . import views

urlpatterns = [
    path("add/",views.StartScraping.as_view()),
    path("get/<int:job_id>", views.GetCoinData.as_view())
]