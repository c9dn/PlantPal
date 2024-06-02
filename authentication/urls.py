from django.urls import path
from .views import *

urlpatterns = [
    path('associate_user/', AssociateUser_API.as_view()),
    path("is_authenticated/", IsAuth_API.as_view()),
    path("authenticate/", EmailAuth_API.as_view()),
    path("authenticate/<email_core>/<verification_code>/", AuthenticateUser_API.as_view()),
]