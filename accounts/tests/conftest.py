import pytest
from django.contrib.auth.models import User, Permission


@pytest.fixture
def user():
    u = User.objects.create_user(username='user', password='password')
    return u
