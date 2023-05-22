import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.forms import LoginForm, AddUserForm
from trip.models import *
from django.test import TestCase
from django.test import Client
from django.test import TestCase


@pytest.mark.django_db
def test_login_get():
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], LoginForm)


@pytest.mark.django_db
def test_login_post(user):
    client = Client()
    url = reverse('login')
    data = {
        'username': 'users',
        'password': 'password'
    }
    response = client.post(url, data)
    assert response.status_code == 200


# Zapytać jak sprawdzić obecnego zalogowanego usera -> potrzebne do tego testu oraz wylogowania


@pytest.mark.django_db
def test_add_user_get():
    client = Client()
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddUserForm)


@pytest.mark.django_db
def test_add_user_post_valid():
    client = Client()
    url = reverse('register')
    data = {
        'username': 'test',
        'password1': 'test1',
        'password2': 'test1',
        'email': 'test@wp.pl'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('index'))


@pytest.mark.django_db
def test_add_user_post_invalid():
    client = Client()
    url = reverse('register')
    data = {
        'username': 'test',
        'password1': 'test1',
        'password2': 'test2',
        'email': 'test@wp.pl'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddUserForm)
