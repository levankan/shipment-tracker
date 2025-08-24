from django.urls import path
from . import views

app_name = "tracking"

urlpatterns = [
    path("", views.submit_tracking, name="submit"),  # home page
]
