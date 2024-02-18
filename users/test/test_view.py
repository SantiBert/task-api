import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from .fixtures import common_user, common_user_token

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_signup(client):
    url = reverse('signup')
    username = "Foo"
    password = "123456789"
    payload = {'username': username, 'password': password}
    response = client.post(url, data=payload, format='json')
    assert response.status_code == 201
    
@pytest.mark.django_db
def test_login(client):
    url = reverse('login')
    username = "Foo"
    password ="123456789"
    payload = {'username': username, 'password': password}
    response = client.post(url, data=payload, format='json')
    assert response.status_code == 200 
    assert 'access' in response.data

@pytest.mark.django_db
def test_refresh_token(client, common_user_token):
    url = reverse('token_refresh')
    refresh_token = common_user_token.get("refresh")
    data = {'refresh': refresh_token}
    response = client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data

@pytest.mark.django_db
def test_logout(client, common_user_token):
    url = reverse('logout')
    access_token = common_user_token.get("access")
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    response = client.post(url)
    assert response.status_code == 205  
    