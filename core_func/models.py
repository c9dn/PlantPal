from django.db import models
from authentication.models import User
import datetime

# Create your models here.

class Community(models.Model):
    comm_name = models.CharField(max_length=100)
    num_of_coordinates = models.IntegerField()
    x_max = models.FloatField()
    x_min = models.FloatField()
    y_max = models.FloatField()
    y_min = models.FloatField()
    added_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    plants_life = models.IntegerField()

class Plant(models.Model):
    plant_lat = models.FloatField()
    plant_long = models.FloatField()
    date_added = models.DateField(default=datetime.date.today())

    image = models.ImageField(upload_to='plants/')
    image_name = models.CharField(max_length=100)
    is_a_plant = models.BooleanField()

    community = models.ForeignKey('Community', on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)

class Coordinate(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    community = models.ForeignKey('Community', on_delete=models.CASCADE)