from django.urls import path
from .views import submit_tracking

app_name = "tracking"

urlpatterns = [
    path("", submit_tracking, name="submit"),
]
