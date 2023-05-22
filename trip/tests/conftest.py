import pytest

from trip.models import Place, Attraction, PlaceAttraction


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
