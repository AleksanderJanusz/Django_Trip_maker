import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from trip.models import *
from django.test import Client


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
    url = reverse('travel_details', kwargs={'pk': travel.id})
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
def test_day_view_logged_out(days):
    client = Client()
    travel = Travel.objects.first()
    days = travel.days_set.first()
    url = reverse('day', kwargs={'trip_pk': travel.pk, 'order': days.order})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_day_view_logged_in_dif_user(days, ten_users):
    client = Client()
    day = Days.objects.first()
    travel = day.travel
    user_invalid = User.objects.last()
    assert travel.user != user_invalid
    client.force_login(user_invalid)
    url = reverse('day', kwargs={'trip_pk': travel.id, 'order': day.order})
    response = client.get(url)
    assert response.status_code == 403


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
def test_day_detail_view_logged_out(days):
    client = Client()
    day = Days.objects.first()
    url = reverse('day_detail', kwargs={'pk': day.id})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_day_detail_view_logged_in_dif_user(days, ten_users):
    client = Client()
    day = Days.objects.first()
    travel = day.travel
    user_invalid = User.objects.last()
    assert travel.user != user_invalid
    client.force_login(user_invalid)
    url = reverse('day_detail', kwargs={'pk': day.id})
    response = client.get(url)
    assert response.status_code == 403


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
    travel = Travel.objects.first()
    url = reverse('travel_delete', kwargs={'pk': travel.id})
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
    travel = Travel.objects.first()
    url = reverse('add_note', kwargs={'pk': travel.id})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_add_note_view_logged_in_dif_user(travels, ten_users):
    client = Client()
    travel = Travel.objects.first()
    user_invalid = User.objects.last()
    assert travel.user != user_invalid
    client.force_login(user_invalid)
    url = reverse('add_note', kwargs={'pk': travel.id})
    response = client.get(url)
    assert response.status_code == 403


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
    note = TravelNotes.objects.first()
    url = reverse('delete_note', kwargs={'pk': note.id})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_delete_note_view_logged_in_valid(notes):
    client = Client()
    travel = Travel.objects.first()
    client.force_login(travel.user)
    note = TravelNotes.objects.filter(trip_id=travel.id).first()
    url = reverse('delete_note', kwargs={'pk': note.id})
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
    note = TravelNotes.objects.filter(trip_id=travel.id).first()
    url = reverse('delete_note', kwargs={'pk': note.id})
    num_notes = len(TravelNotes.objects.all())
    response = client.get(url)
    assert response.status_code == 403
    assert num_notes == len(TravelNotes.objects.all())


@pytest.mark.django_db
def test_edit_note_view_logged_out(notes):
    client = Client()
    note = TravelNotes.objects.first()
    url = reverse('edit_note', kwargs={'pk': note.id})
    response = client.get(url)
    assert response.status_code == 302
    redirect_url = reverse('login')
    assert response.url.startswith(redirect_url)


@pytest.mark.django_db
def test_edit_note_view_logged_in_dif_user(notes, ten_users):
    client = Client()
    note = TravelNotes.objects.first()
    travel = Travel.objects.get(pk=note.trip_id)
    user_invalid = User.objects.last()
    assert travel.user != user_invalid
    client.force_login(user_invalid)
    url = reverse('edit_note', kwargs={'pk': note.id})
    response = client.get(url)
    assert response.status_code == 403


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
