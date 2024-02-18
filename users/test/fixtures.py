import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password

FAKE_USER_USERNAME = "Foo"
FAKE_USER_PASSWORD = "123456789"
FAKE_USER_EMAIL = "user@quorumit.com"

TEST_USERS_LIST = [
    {
        "username": "FOO",
        "password": "123456789",
        "email": "foo@gmail.com",
    },
    {
        "username": "FUU",
        "password": "123456789",
        "email": "fuu@gmail.com"
    },
]

def generate_refresh_token(user):
    refresh_token = RefreshToken.for_user(user)
    return str(refresh_token)

def generate_access_token(user):
    token_serializer = TokenObtainPairSerializer()
    tokens = token_serializer.get_token(user)
    return str(tokens.access_token)

@pytest.mark.django_db
@pytest.fixture
def common_user():
    user_model = get_user_model()
    for user_data in TEST_USERS_LIST:
        user_data['password'] = make_password(user_data['password'])
        user, created = user_model.objects.get_or_create(**user_data)
    return user_model.objects.first()

@pytest.mark.django_db
@pytest.fixture
def common_user_token(common_user):
    access_token = generate_access_token(common_user)
    refresh_token = generate_refresh_token(common_user)
    return {
        "access": access_token,
        "refresh": refresh_token,
        "user": common_user,
    }
