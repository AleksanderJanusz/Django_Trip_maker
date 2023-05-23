import pytest
from django.urls import reverse

from trip.forms import AddPlaceForm
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
    places_fixture_distinct = set([p.country for p in places])
    places_fixture = [p for p in places_fixture_distinct]
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


@pytest.mark.django_db
def test_attraction_details_view(attractions):
    client = Client()
    attraction = Attraction.objects.first()
    url = reverse('attractions', kwargs={'pk': attraction.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['attraction'] == attraction


@pytest.mark.django_db
def test_add_place_logout():
    client = Client()
    url = reverse('add_place')
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_add_place_login_get(users):
    client = Client()
    client.force_login(users)
    url = reverse('add_place')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddPlaceForm)


@pytest.mark.django_db
def test_add_place_login_post(users):
    client = Client()
    client.force_login(users)
    url = reverse('add_place')
    data = {
        'name': 'name',
        'country': 'country',
        'description': 'description'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    redirect_url = reverse('index')
    assert response.url.startswith(redirect_url)
    place = Place.objects.first()
    assert place.name == 'name'.capitalize()
    assert place.country == 'country'.capitalize()


@pytest.mark.django_db
@pytest.mark.parametrize("data, result",
                         [({
                               'name': '',
                               'country': 'country',
                               'description': 'description'
                           }, 200),
                             ({
                                  'name': 'name',
                                  'country': '',
                                  'description': 'description'
                              }, 200),
                             ({
                                  'name': 'name',
                                  'country': 'country',
                                  'description': ''
                              }, 302)])
def test_add_place_login_post_if_valid(users, data, result):
    client = Client()
    client.force_login(users)
    url = reverse('add_place')
    response = client.post(url, data)
    assert response.status_code == result

