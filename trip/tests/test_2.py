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
