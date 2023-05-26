from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class TravelNotes(models.Model):
    GENRE_CHOICES = (
        (0, 'before the travel'),
        (1, 'during the travel'),
        (2, 'after the travel'),
    )
    note = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(choices=GENRE_CHOICES, default=0)
    trip = models.ForeignKey('Travel', on_delete=models.CASCADE)


class Travel(models.Model):
    GENRE_CHOICES = (
        (0, 'Planowanie'),
        (1, 'W drogę!'),
        (2, 'Zakończona'),
    )
    name = models.CharField(max_length=255)
    status = models.IntegerField(choices=GENRE_CHOICES, default=0)
    place_attraction = models.ManyToManyField('PlaceAttraction', through='Days')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    attraction = models.ManyToManyField('Attraction', through='PlaceAttraction')

    def __str__(self):
        return self.name


class Attraction(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time = models.CharField(null=True, max_length=255)

    def __str__(self):
        return self.name


class Cost(models.Model):
    persons = models.IntegerField(default=1)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cost)


class PlaceAttraction(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.place.name} - {self.attraction.name}'


class Days(models.Model):
    place_attraction = models.ForeignKey(PlaceAttraction, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.order)
