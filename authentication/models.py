from django.db import models

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=100, unique=True)
    email_core = models.CharField(max_length=100, unique=True)
    email_provider = models.CharField(max_length=100)
    is_banned = models.BooleanField(default=0)
    is_authenticated = models.BooleanField(default=0)
    curr_auth_code = models.CharField(max_length=10)
    requested_auth = models.BooleanField()
    community_name = models.CharField(max_length=100)
    authenticated_datetime = models.DateTimeField()