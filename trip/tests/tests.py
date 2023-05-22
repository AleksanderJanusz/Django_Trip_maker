import pytest
from django.urls import reverse
from trip.models import *
from django.test import TestCase
from django.test import Client


def test_index_view():
    client = Client()
    url = reverse('index')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_place_view_order(places):
    client = Client()
    url = reverse('places')
    response = client.get(url)
    places_fixture = [p.country for p in places]
    places_fixture.sort()
    places_response = [p.country for p in response.context['places']]
    assert response.status_code == 200
    assert places_response == places_fixture


@pytest.mark.django_db
def test_place_view_distinct(places):
    client = Client()
    url = reverse('places')
    response = client.get(url)
    places_fixture_distinct = set([p.country for p in places])
    places_response = response.context['places']
    assert response.status_code == 200
    assert len(places_response) == len(places_fixture_distinct)


@pytest.mark.django_db
def test_place_api_places_by_country(places):
    client = Client()
    place = Place.objects.first()
    url = reverse('places_by_country_api') + f'?place_country_api={place.id}'
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()[0]['id'] == place.id
    assert response.json()[0]['name'] == place.name


@pytest.mark.django_db
def test_place_api_attraction_by_place(attractions_places):
    client = Client()
    place = Place.objects.first()
    url = reverse('attraction_by_place_api') + f'?place_api={place.id}'
    response = client.get(url)
    assert response.status_code == 200
    attraction_fixture_names = [attract.name for attract in place.attraction.all()]
    attraction_fixture_desc = [attract.description for attract in place.attraction.all()]
    attraction_response_names = [attract['name'] for attract in response.json()]
    attraction_response_desc = [attract['description'] for attract in response.json()]
    assert attraction_response_names == attraction_fixture_names
    assert attraction_response_desc == attraction_fixture_desc

