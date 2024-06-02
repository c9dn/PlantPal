from django.urls import path
from .views import *

urlpatterns = [
    path('community_image/', CommunityImageAPI.as_view()),
    path("add_plant/", PlantAPI.as_view()),
    path("add_community/", CommunityAPI.as_view()),
]
