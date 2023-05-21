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
