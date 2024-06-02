from django.urls import path, include
from .views import *

urlpatterns = [
    path("leaderboard/", LeaderboardAPI.as_view())
]