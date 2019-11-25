from django.urls import path
from rooms.views import HomeView

app_name = "cores"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
