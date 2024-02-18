import pytest
from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .fixtures import (
    common_user, 
    common_user_token
    )

# Fixture to create an instance of APIClient
@pytest.fixture
def client():
    return APIClient()

# Test case for user signup
@pytest.mark.django_db
def test_signup(client):
    # Prepare data for signup
    url = reverse('signup')
    username = "Foo"
    password = "123456789"
    payload = {'username': username, 'password': password}
    
    # Make POST request to signup endpoint
    response = client.post(url, data=payload, format='json')
    
    # Assert that the response status is 201 Created
    assert response.status_code == status.HTTP_201_CREATED

# Test case for user login
@pytest.mark.django_db
def test_login(client, common_user):
    # Prepare data for login
    url = reverse('login')
    username = "FAA"
    password = "123456789"
    
    # Create a user instance in the database
    user_model = get_user_model()
    user_data ={
        "username": username,
        "password": password,
        "email": "faa@gmail.com"
    }
    user_data['password'] = make_password(user_data['password'])
    user, created = user_model.objects.get_or_create(**user_data)
    
    payload = {'username': username, 'password': password}
    
    # Make POST request to login endpoint
    response = client.post(url, data=payload, format='json')
   
    # Assert that the response status is 200 OK and contains 'access' token
    assert response.status_code == status.HTTP_200_OK 
    assert 'access' in response.data

# Test case for refreshing an access token
@pytest.mark.django_db
def test_refresh_token(client, common_user_token):
    # Prepare data for token refresh
    url = reverse('token_refresh')
    refresh_token = common_user_token.get("refresh")
    data = {'refresh': refresh_token}
    
    # Make POST request to token refresh endpoint
    response = client.post(url, data, format='json')
    
    # Assert that the response status is 200 OK and contains 'access' token
    assert response.status_code == status.HTTP_200_OK 
    assert 'access' in response.data

# Test case for user logout
@pytest.mark.django_db
def test_logout(client, common_user_token):
    # Prepare data for logout
    url = reverse('logout')
    access_token = common_user_token.get("access")
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    
    # Make POST request to logout endpoint
    response = client.post(url)  # Realizar una solicitud POST a la URL de cierre de sesión
    
    # Assert that the response status is 205 Reset Content
    assert response.status_code == status.HTTP_205_RESET_CONTENT 
