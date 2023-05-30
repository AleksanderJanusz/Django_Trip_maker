import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from trip.forms import AddPlaceForm, AddAttractionForm, AddTravelForm, AddDaysForm
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
def test_add_place_logged_out():
    client = Client()
    url = reverse('add_place')
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_add_place_logged_in_get(users):
    client = Client()
    client.force_login(users)
    url = reverse('add_place')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddPlaceForm)


@pytest.mark.django_db
def test_add_place_logged_in_post(users):
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
def test_add_place_logged_in_post_if_valid(users, data, result):
    client = Client()
    client.force_login(users)
    url = reverse('add_place')
    response = client.post(url, data)
    assert response.status_code == result


@pytest.mark.django_db
def test_add_attraction_logged_out():
    client = Client()
    url = reverse('add_attraction')
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_add_place_logged_in_get(users, places):
    client = Client()
    client.force_login(users)
    url = reverse('add_attraction')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddAttractionForm)
    response_places = [place for place in response.context['places']]
    places_all = [place for place in Place.objects.all()]
    assert response_places == places_all


@pytest.mark.django_db
def test_add_attraction_logged_in_post_checked_valid(users, places):
    client = Client()
    client.force_login(users)
    url = reverse('add_attraction')
    place = Place.objects.first().id
    data = {
        'name': 'name',
        'description': 'description',
        'time': 'time',
        'place': place,
        'checkbox': 'True',
        'persons': '1',
        'from': '10',
        'to': '20',
    }
    len_attraction = len(Attraction.objects.all())
    len_place = len(PlaceAttraction.objects.all())
    len_cost = len(Cost.objects.all())
    response = client.post(url, data)
    assert response.status_code == 302
    redirect_url = reverse('index')
    assert response.url.startswith(redirect_url)
    assert len(Attraction.objects.all()) == len_attraction + 1
    assert len(PlaceAttraction.objects.all()) == len_place + 1
    assert len(Cost.objects.all()) == len_cost + 2


@pytest.mark.django_db
def test_add_attraction_logged_in_post_un_checked_valid(users, places):
    client = Client()
    client.force_login(users)
    url = reverse('add_attraction')
    place = Place.objects.first().id
    data = {
        'name': 'name',
        'description': 'description',
        'time': 'time',
        'place': place,
        'checkbox': '',
        'persons': '1',
        'from': '10',
        'to': '0',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    redirect_url = reverse('index')
    assert len(Cost.objects.all()) == 1
    assert response.url.startswith(redirect_url)
    assert len(Attraction.objects.all()) == 1
    assert len(PlaceAttraction.objects.all()) == 1


@pytest.mark.django_db
@pytest.mark.parametrize('data, result',
                         [({'name': '', 'description': 'description', 'time': 'time', 'place': '1',
                            'checkbox': 'True', 'persons': '1', 'from': '10', 'to': '0', }, 200),
                          ({'name': 'name', 'description': 'description', 'time': 'time', 'place': '1',
                            'checkbox': 'True', 'persons': '-1', 'from': '10', 'to': '0', }, 200),
                          ({'name': 'name', 'description': 'description', 'time': 'time', 'place': '1',
                            'checkbox': 'True', 'persons': '1', 'from': '-1', 'to': '0', }, 200),
                          ({'name': 'name', 'description': 'description', 'time': 'time', 'place': '1',
                            'checkbox': 'True', 'persons': '1', 'from': '10', 'to': '-1', }, 200),
                          ({'name': 'name', 'description': 'description', 'time': 'time', 'place': '1',
                            'checkbox': 'True', 'persons': '', 'from': '10', 'to': '-1', }, 200),
                          ({'name': 'name', 'description': 'description', 'time': 'time', 'place': '1',
                            'checkbox': 'True', 'persons': '1', 'from': '', 'to': '-1', }, 200),
                          ({'name': 'name', 'description': 'description', 'time': 'time', 'place': '1',
                            'checkbox': 'True', 'persons': '1', 'from': '10', 'to': '', }, 200)
                          ])
def test_add_attraction_logged_in_post_checked_in_valid(users, places, data, result):
    client = Client()
    client.force_login(users)
    url = reverse('add_attraction')
    response = client.post(url, data)
    assert response.status_code == result


@pytest.mark.django_db
def test_attraction_place_api(attractions_places):
    client = Client()
    place = Place.objects.first()
    url = reverse('attraction_place_api') + f'?place_api={place.id}'
    response = client.get(url)
    assert response.status_code == 200
    attractions_places_id = PlaceAttraction.objects.filter(place_id=place.id)
    attractions_places_id = [place.id for place in attractions_places_id]
    attractions_places_id_json = [place['id'] for place in response.json()]
    assert attractions_places_id_json == attractions_places_id


@pytest.mark.django_db
def test_add_travel_logged_out():
    client = Client()
    url = reverse('add_travel')
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_add_travel_logged_in_get(users):
    client = Client()
    client.force_login(users)
    url = reverse('add_travel')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddTravelForm)


@pytest.mark.django_db
def test_add_travel_logged_in_post(users):
    client = Client()
    client.force_login(users)
    url = reverse('add_travel')
    data = {
        'name': 'name',
        'status': '1',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    travel_id = Travel.objects.last().id
    redirect_url = reverse('add_travel_part2', kwargs={'pk': travel_id})
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_add_travel2_logged_in_get(users, travels, places):
    client = Client()
    client.force_login(users)
    travel = Travel.objects.first()
    url = reverse('add_travel_part2', kwargs={'pk': travel.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddDaysForm)
    assert response.context['trip'] == travel

    response_places = [place for place in response.context['places']]
    my_places = [place for place in Place.objects.all().order_by('country').distinct('country')]
    assert response_places == my_places

    response_days = [day for day in response.context['days']]
    my_days = [day for day in Days.objects.filter(travel_id=travel.pk)]
    assert response_days == my_days

    response_orders = [order for order in response.context['orders']]
    my_orders = [order for order in Days.objects.filter(travel_id=travel.pk).distinct('order')]
    assert response_orders == my_orders


@pytest.mark.django_db
def test_add_travel2_logged_out():
    client = Client()
    url = reverse('add_travel_part2', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_add_travel2_logged_in_post(travels, attractions_places):
    client = Client()
    travel = Travel.objects.first()
    user = travel.user
    client.force_login(user)
    attraction_id = PlaceAttraction.objects.first().id
    url = reverse('add_travel_part2', kwargs={'pk': travel.pk})
    data = {
        'order': '1',
        'place_attraction': attraction_id,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    day = Days.objects.last()
    assert day.travel == travel
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_travel_view_logged_out():
    client = Client()
    url = reverse('travels')
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_travel_view_logged_in_get(ten_users, many_travels):
    client = Client()
    user = User.objects.first()
    client.force_login(user)
    url = reverse('travels')
    response = client.get(url)
    assert response.status_code == 200
    travels = Travel.objects.filter(user_id=user.id).order_by('name')
    assert [travel.user == user for travel in response.context['travels']]
    assert len(travels) == len(response.context['travels'])


@pytest.mark.django_db
def test_travel_details_view_logged_out():
    client = Client()
    url = reverse('travel_details', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_travel_details_view_logged_in_get(notes):
    client = Client()
    travel = Travel.objects.last()
    user = travel.user
    client.force_login(user)
    url = reverse('travel_details', kwargs={'pk': travel.pk})
    response = client.get(url)
    my_days = Days.objects.filter(travel_id=travel.pk)
    assert response.status_code == 200
    assert response.context['trip'] == travel
    assert [day for day in response.context['days']] == [day for day in my_days]
    assert [order for order in response.context['orders']] == [order for order in my_days.distinct('order')]
    assert [note for note in response.context['notes']] == [note for note in
                                                            TravelNotes.objects.filter(trip_id=travel.id)]


@pytest.mark.django_db
def test_travel_details_view_logged_in_post(notes):
    client = Client()
    travel = Travel.objects.first()
    user = travel.user
    client.force_login(user)
    url = reverse('travel_details', kwargs={'pk': travel.pk})
    response = client.post(url)
    my_days = Days.objects.filter(travel_id=travel.pk)
    assert response.status_code == 200
    assert response.context['trip'] == travel
    assert [day for day in response.context['days']] == [day for day in my_days]
    assert [order for order in response.context['orders']] == [order for order in my_days.distinct('order')]
    assert [note for note in response.context['notes']] == [note for note in
                                                            TravelNotes.objects.filter(trip_id=travel.id)]


@pytest.mark.django_db
def test_day_view_logged_out():
    client = Client()
    url = reverse('day', kwargs={'trip_pk': 1, 'order': 1})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_day_view_logged_in_get(days):
    client = Client()
    travel = Travel.objects.first()
    user = travel.user
    days = travel.days_set.first()
    client.force_login(user)
    url = reverse('day', kwargs={'trip_pk': travel.pk, 'order': days.order})
    response = client.get(url)
    assert response.status_code == 200
    assert [day for day in response.context['days']] == [day for day in Days.objects.filter(travel_id=travel.pk).filter(
        order=days.order)]


@pytest.mark.django_db
def test_day_detail_view_logged_out():
    client = Client()
    url = reverse('day_detail', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_day_detail_view_logged_in_get(days):
    client = Client()
    travel = Travel.objects.first()
    user = travel.user
    day = travel.days_set.first()
    client.force_login(user)
    url = reverse('day_detail', kwargs={'pk': day.id})
    response = client.get(url)
    assert response.status_code == 200


# JAK WEJSC W SUCCESS_URL


@pytest.mark.django_db
def test_delete_day_view_logged_out(days):
    client = Client()
    day = Days.objects.first()
    num_days = len(Days.objects.all())
    url = reverse('day_delete', kwargs={'pk': day.id})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)
    assert num_days == len(Days.objects.all())


@pytest.mark.django_db
def test_delete_day_view_logged_in_valid(days):
    client = Client()
    day = Days.objects.first()
    order = day.order
    trip_pk = day.travel_id
    num_days = len(Days.objects.all())
    user = day.travel.user
    client.force_login(user)
    url = reverse('day_delete', kwargs={'pk': day.id})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('day_detail_delete', kwargs={'order': order, 'trip_pk': trip_pk})
    assert response.url.startswith(redirect_url)
    assert num_days == len(Days.objects.all()) + 1


@pytest.mark.django_db
def test_delete_day_view_logged_in_invalid(days, ten_users):
    client = Client()
    day = Days.objects.first()
    order = day.order
    trip_pk = day.travel_id
    num_days = len(Days.objects.all())
    user = ten_users[0]
    client.force_login(user)
    url = reverse('day_delete', kwargs={'pk': day.id})
    response = client.get(url)
    assert response.status_code == 403
    assert num_days == len(Days.objects.all())


@pytest.mark.django_db
def test_days_delete_view_logged_out(days):
    client = Client()
    url = reverse('day_detail_delete', kwargs={'trip_pk': 1, 'order': 1})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_days_delete_view_logged_in(days):
    client = Client()
    travel = Travel.objects.first()
    day = Days.objects.filter(travel_id=travel.id).first()
    user = travel.user
    client.force_login(user)
    url = reverse('day_detail_delete', kwargs={'trip_pk': travel.id, 'order': day.order})
    response = client.get(url)
    assert response.status_code == 200
    assert [day for day in response.context['days']] == [day for day in Days.objects.filter(travel_id=travel.id).filter(
        order=day.order)]


@pytest.mark.django_db
def test_delete_travel_view_logged_out(days):
    client = Client()
    url = reverse('travel_delete', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_delete_travel_view_logged_in_valid(many_travels):
    client = Client()
    travel = Travel.objects.first()
    user = travel.user
    client.force_login(user)
    num_travels = len(Travel.objects.all())
    url = reverse('travel_delete', kwargs={'pk': travel.pk})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('travels')
    assert response.url.startswith(redirect_url)
    assert num_travels == len(Travel.objects.all()) + 1


@pytest.mark.django_db
def test_delete_travel_view_logged_in_invalid(many_travels):
    client = Client()
    travel = Travel.objects.first()
    user = User.objects.last()
    assert travel.user != user  # make sure they are different users
    client.force_login(user)
    num_travels = len(Travel.objects.all())
    url = reverse('travel_delete', kwargs={'pk': travel.pk})
    response = client.get(url)
    assert response.status_code == 403
    assert num_travels == len(Travel.objects.all())


@pytest.mark.django_db
def test_add_note_view_logged_out(travels):
    client = Client()
    url = reverse('add_note', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_add_note_view_logged_in_get(travels):
    client = Client()
    travel = Travel.objects.first()
    client.force_login(travel.user)
    url = reverse('add_note', kwargs={'pk': travel.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_note__view_logged_in_post(travels):
    client = Client()
    travel = Travel.objects.first()
    client.force_login(travel.user)
    data = {
        'note': 'note'
    }
    num_notes = len(TravelNotes.objects.all())
    url = reverse('add_note', kwargs={'pk': travel.pk})
    response = client.post(url, data)
    assert response.status_code == 302
    redirect_url = reverse('travel_details', kwargs={'pk': travel.pk})
    assert response.url.startswith(redirect_url)
    assert num_notes + 1 == len(TravelNotes.objects.all())
    assert TravelNotes.objects.last().trip_id == travel.pk
    assert TravelNotes.objects.last().status == travel.status


@pytest.mark.django_db
def test_delete_note_view_logged_out(notes):
    client = Client()
    url = reverse('delete_note', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_delete_note_view_logged_in_valid(notes):
    client = Client()
    travel = Travel.objects.first()
    client.force_login(travel.user)
    url = reverse('delete_note', kwargs={'pk': travel.id})
    num_notes = len(TravelNotes.objects.all())
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('travel_details', kwargs={'pk': travel.id})
    assert response.url.startswith(redirect_url)
    assert num_notes == len(TravelNotes.objects.all()) + 1


@pytest.mark.django_db
def test_delete_note_view_logged_in_invalid(notes, ten_users):
    client = Client()
    travel = Travel.objects.first()
    client.force_login(ten_users[0])
    url = reverse('delete_note', kwargs={'pk': travel.id})
    num_notes = len(TravelNotes.objects.all())
    response = client.get(url)
    assert response.status_code == 403
    assert num_notes == len(TravelNotes.objects.all())


@pytest.mark.django_db
def test_edit_note_view_logged_out(notes):
    client = Client()
    url = reverse('edit_note', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_edit_note_view_logged_in_invalid(notes, ten_users):
    client = Client()
    note = TravelNotes.objects.first()
    client.force_login(ten_users[0])
    url = reverse('edit_note', kwargs={'pk': note.id})
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_note_view_logged_in_post(notes):
    client = Client()
    note = TravelNotes.objects.first()
    travel = Travel.objects.get(pk=note.trip_id)
    client.force_login(travel.user)
    data = {
        'note': 'note edited',
        'status': '2'
    }
    url = reverse('edit_note', kwargs={'pk': note.id})
    response = client.post(url, data)
    assert response.status_code == 302
    redirect_url = reverse('travel_details', kwargs={'pk': travel.id})
    assert response.url.startswith(redirect_url)
    assert TravelNotes.objects.get(pk=note.pk).note == 'note edited (edytowany)'


@pytest.mark.django_db
def test_edit_note_view_logged_in_get(notes):
    client = Client()
    note = TravelNotes.objects.first()
    travel = Travel.objects.get(pk=note.trip_id)
    client.force_login(travel.user)
    data = {
        'note': 'note edited',
        'status': '2'
    }
    url = reverse('edit_note', kwargs={'pk': note.id})
    response = client.post(url, data)
    assert response.status_code == 302
    response = client.get(url)
    assert response.status_code == 200
    assert TravelNotes.objects.get(pk=note.pk).note == 'note edited (edytowany)'
    assert response.context['form']['note'].initial == 'note edited'


@pytest.mark.django_db
def test_travel_status_serializer_get(many_travels):
    client = APIClient()
    travel = Travel.objects.first()
    url = reverse('travels_status', kwargs={'pk': travel.pk})
    response = client.get(url, {}, format='json')

    assert response.status_code == 200
    assert response.data['name'] == travel.name
    assert response.data['user'] == travel.user_id
    assert response.data['status'] == travel.status
    assert response.data['choice'] == travel.GENRE_CHOICES


@pytest.mark.django_db
def test_travel_status_serializer_patch(many_travels):
    client = APIClient()
    travel = Travel.objects.first()
    url = reverse('travels_status', kwargs={'pk': travel.pk})
    response = client.patch(url, {'name': 'new_name'}, format='json')
    assert response.status_code == 200
    assert response.data['name'] == 'new_name'


@pytest.mark.django_db
def test_travel_status_serializer_delete(many_travels):
    client = APIClient()
    travel = Travel.objects.first()
    travel_id = travel.id
    url = reverse('travels_status', kwargs={'pk': travel.pk})
    response = client.delete(url, {}, format='json')
    assert response.status_code == 204
    try:
        Travel.objects.get(pk=travel_id)
        assert False
    except Travel.DoesNotExist:
        assert True


@pytest.mark.django_db
def test_country_distinct_api(places):
    client = Client()
    url = reverse('countries_api')
    response = client.get(url)
    assert response.status_code == 200
    places_id_json = [place['id'] for place in response.json()]
    places_id = [place.id for place in Place.objects.all().order_by('country').distinct('country')]
    assert places_id == places_id_json


@pytest.mark.django_db
def test_places_api(places):
    client = Client()
    url = reverse('places_api')
    response = client.get(url)
    assert response.status_code == 200
    places_id_json = [place['id'] for place in response.json()]
    places_id = [place.id for place in Place.objects.all()]
    assert places_id == places_id_json


@pytest.mark.django_db
def test_attractions_api(attractions):
    client = Client()
    url = reverse('attractions_api')
    response = client.get(url)
    assert response.status_code == 200
    attractions_id_json = [attraction['id'] for attraction in response.json()]
    attractions_id = [attraction.id for attraction in Attraction.objects.all()]
    assert attractions_id_json == attractions_id
