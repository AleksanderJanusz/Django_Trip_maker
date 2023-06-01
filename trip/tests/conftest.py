from random import randint

import pytest
from django.contrib.auth.models import User

from trip.models import Place, Attraction, PlaceAttraction, Travel, Days, TravelNotes


@pytest.fixture
def places():
    return [Place.objects.create(name='aPlace', country='aCountry', description='aDescription'),
            Place.objects.create(name='zPlace', country='zCountry', description='zDescription'),
            Place.objects.create(name='zPlace', country='zCountry', description='zDescription'),
            Place.objects.create(name='dPlace', country='dCountry', description='dDescription')]


@pytest.fixture
def attractions():
    return [Attraction.objects.create(name=f'attraction{i}',
                                      description=f'description{i}',
                                      time=f'time{i}') for i in range(15)]


@pytest.fixture
def attractions_places(places, attractions):
    lst = []
    for place in places:
        place.attraction.set(attractions)
        lst.append(place)
    return lst


@pytest.fixture
def users():
    return User.objects.create_user(username='user', password='password')


@pytest.fixture
def travels(users):
    return Travel.objects.create(name='name', user=users)


@pytest.fixture
def ten_users():
    return [User.objects.create_user(username=f'user{i}', password=f'password{i}') for i in range(10)]


@pytest.fixture
def many_travels(ten_users):
    return [[Travel.objects.create(name=f'name{j}', user=i) for j in range(5)] for i in ten_users]


@pytest.fixture
def days(travels, attractions_places):
    return [Days.objects.create(order=randint(1, 7), travel_id=travels.id,
                                place_attraction_id=PlaceAttraction.objects.all()[i].id) for i in range(4)]


@pytest.fixture
def notes(days):
    travel = Travel.objects.first()
    return [TravelNotes.objects.create(note=f'note{i}', status=0, trip_id=travel.id) for i in range(10)]

