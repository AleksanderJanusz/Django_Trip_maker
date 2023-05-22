import pytest
from django.contrib.auth.models import User, Permission


@pytest.fixture
def user():
    u = User.objects.create(username='user', password='password')
    return u
