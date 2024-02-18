import pytest

from rest_framework.test import APIClient
from rest_framework import status
from users.test.fixtures import common_user, common_user_token

from django.urls import reverse

from task.models import Task

# ===========================================
# ============== CREATE TASK ================
# ===========================================

# Test creating a task successfully
@pytest.mark.django_db
def test_create_task_successfully(common_user_token):
    
    # Extract user information and access token from fixture
    user = common_user_token.get("user")
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Prepare task data
    name = f"{user.username}’s Task Name"
    description = f"{user.username}’s Task Description"
    payload = {"name": name, "description": description}
    
    # Make POST request to create a task
    url = reverse("create-task")
    response = client.post(url, data=payload, format="json")
    
    # Assert that the task is created successfully
    assert response.status_code == status.HTTP_200_OK
    task_id = response.json().get("data").get("id")
    task = Task.objects.get(id=task_id)
    assert task.name == name
    assert task.description == description

# Test creating a task with a name that already exists
@pytest.mark.django_db
def test_create_task_whit_repite_name(common_user_token):
    
    # Extract user information and access token from fixture
    user = common_user_token.get("user")
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Prepare task data
    name = f"{user.username}'s Task Name"
    description = f"{user.username}'s Task Description"
    
    # Create a task with the same name
    task = Task.objects.create(name=name, description=description)
    
    # Attempt to create another task with the same name
    payload = {"name": name, "description": description}
    url = reverse("create-task")
    response = client.post(url, data=payload, format="json")
    
    # Assert that the second task creation fails due to duplicate name
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Change the name and try again
    second_name = "Task Renamed"
    task.name = second_name
    task.save()
    second_response = client.post(url, data=payload, format="json")
    
    # Assert that the second task creation succeeds after changing the name
    assert second_response.status_code == status.HTTP_200_OK
    second_task_id = second_response.json().get("data").get("id")
    second_task = Task.objects.get(id=second_task_id)
    assert second_task.name == name
    assert second_task.description == description

# Test creating a task with an invalid payload
@pytest.mark.django_db
def test_create_task_with_invalid_payload(common_user_token):
    
    # Extract access token from fixture
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Invalid payload missing the 'description' field
    invalid_payload = {"name": "Task Name"}
    
    # Attempt to create a task with the invalid payload
    url = reverse("create-task")
    response = client.post(url, data=invalid_payload, format="json")
    
    # Assert that the task creation fails due to missing 'description' field
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# Test creating a task without authentication
@pytest.mark.django_db
def test_create_task_without_authentication():
    
    # Create API client without setting authorization header
    client = APIClient()
    
    # Prepare task data
    payload = {"name": "Task Name", "description": "Task Description"}
    
    # Attempt to create a task without authentication
    url = reverse("create-task")
    response = client.post(url, data=payload, format="json")
    
    # Assert that the task creation fails due to lack of authentication
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
# ===========================================
# ============== DETAIL TASK ================
# ===========================================

# Test get a existing task successfully
@pytest.mark.django_db
def test_get_existing_task(common_user_token):
    # Extract access token from fixture
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Create a task in the database
    name = "Task Name"
    description = "Task Description"
    task = Task.objects.create(name=name, description=description)
    
    # Prepare URL for retrieving the task
    url = reverse("task", kwargs={"pk": task.id})
    
    # Make GET request to retrieve the task
    response = client.get(url)
    
    # Assert that the task is retrieved successfully
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("task").get("name") == name
    assert response.data.get("task").get("description") == description

# Test get a not existing task
@pytest.mark.django_db
def test_get_non_existing_task(common_user_token):
    # Extract access token from fixture
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    # Prepare URL for retrieving a non-existing task
    url = reverse("task", kwargs={"pk": 999})
    
    # Make GET request to retrieve the non-existing task
    response = client.get(url)
    
    # Assert that the request returns a 404 error and the expected error message
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data.get("error") == "Task does not exist"

# Test get a task without authentication
@pytest.mark.django_db
def test_get_task_without_authentication():
    
    # Create API client without setting authorization header
    client = APIClient()
    
    # Create a task in the database
    name = "Task Name"
    description = "Task Description"
    task = Task.objects.create(name=name, description=description)
    
    # Prepare URL for retrieving the task
    url = reverse("task", kwargs={"pk": task.id})
    response = client.get(url)
    
    # Make GET request to retrieve the task without authentication
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# ===========================================
# ============== DELETE TASK ================
# ===========================================

# Test delete a task successfully
@pytest.mark.django_db
def test_delete_task(common_user_token):
    # Extract access token from fixture
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Create a task in the database
    name = "Task Name"
    description = "Task Description"
    task = Task.objects.create(name=name, description=description)
    
    # Prepare URL for deleting the task
    url = reverse("task", kwargs={"pk": task.id})
    
    # Make DELETE request to delete the task
    response = client.delete(url)
    
    # Assert that the task is deleted successfully and no longer exists
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("message") == "Task deleted"
    assert not Task.objects.filter(pk=task.pk, is_active=True).exists()

# Test delete a not existing task
@pytest.mark.django_db
def test_delete_non_existing_task(common_user_token):
    # Extract access token from fixture
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Prepare URL for deleting a non-existing task
    url = reverse("task", kwargs={"pk": 999})
    
    # Make DELETE request to delete the non-existing task
    response = client.delete(url)
    
    # Assert that the request returns a 404 error and the expected error message
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data.get("error") == "Task does not exist"

# Test delete a task without authentication
@pytest.mark.django_db
def test_delete_task_without_authentication():
    # Create API client and set authorization header
    client = APIClient()
    
    # Create a task in the database
    name = "Task Name"
    description = "Task Description"
    task = Task.objects.create(name=name, description=description)
    
    # Prepare URL for deleting the task
    url = reverse("task", kwargs={"pk": task.id})
    
    # Make DELETE request to delete the task without authentication
    response = client.delete(url)
    
    # Assert that the task deletion fails due to lack of authentication
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# ===========================================
# ============== TASK LIST ==================
# ===========================================

# Test get a tasks list successfully
@pytest.mark.django_db
def test_get_task_list(common_user_token):
    # Extract access token from fixture
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Create two tasks in the database
    Task.objects.create(name="Task 1", description="Task Description 1")
    Task.objects.create(name="Task 2", description="Task Description 2")
    
    # Prepare URL for retrieving the task list
    url = reverse("task-list")
    
    # Make GET request to retrieve the task list
    response = client.get(url)
    
    # Assert that the request is successful
    assert response.status_code == status.HTTP_200_OK
    
    # Retrieve tasks from the response data
    tasks = response.data.get('tasks')
    
    # Assert that the task list contains two tasks
    assert len(tasks) == 2

# Test get a empy tasks list
@pytest.mark.django_db
def test_empty_task_list(common_user_token):
    # Extract access token from fixture
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Prepare URL for retrieving an empty task list
    url = reverse("task-list")
    
    # Make GET request to retrieve the empty task list
    response = client.get(url)
    
    # Assert that the request is successfull
    assert response.status_code == status.HTTP_200_OK
    
    tasks = response.data.get('tasks')
    
    # Assert that the task list is empty
    assert len(tasks) == 0

# Test get a tasks list without authentication
@pytest.mark.django_db
def test_get_task_list_without_authentication():
    # Create API client without setting authorization header
    client = APIClient()
    
    # Create two tasks in the database
    Task.objects.create(name="Task 1", description="Task Description 1")
    Task.objects.create(name="Task 2", description="Task Description 2")
    
    # Prepare URL for retrieving the task list without authentication
    url = reverse("task-list")
    
    # Make GET request to retrieve the task list without authentication
    response = client.get(url)
    
    # Assert that the request returns a 401 error due to lack of authentication
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    

# ===========================================
# ============== EDIT TASK ==================
# ===========================================

@pytest.mark.django_db
def test_edit_task_successfully(common_user_token):
    # Extract user and access token from fixture
    user = common_user_token.get("user")
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Create a task in the database
    task = Task.objects.create(name="Task 1", description="Task Description 1")
    
    # Prepare updated task data
    second_name = "Task Renamed"
    second_description = "Task Description edited"
    payload = {"name": second_name, "description": second_description}
    
    # Prepare URL for editing the task
    url = reverse("edit-task", kwargs={"pk": task.id})
    
    # Make PUT request to edit the task
    response = client.put(url, data=payload, format="json")
    
    # Assert that the request is successful
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_edit_non_existing_task(common_user_token):
    # Extract user and access token from fixture
    user = common_user_token.get("user")
    access_token = common_user_token.get("access")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Prepare task data
    name = f"{user.username}'s Task Name"
    description = f"{user.username}'s Task Description"
    payload = {"name": name, "description": description}
    
    # Prepare URL for editing a non-existing task
    url = reverse("edit-task", kwargs={"pk": 999}) 
    
    # Make PUT request to edit the non-existing task
    response = client.put(url, data=payload, format="json")
    
    # Assert that the request returns a 400 error due to non-existence of the task
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data.get("error") == "Task does not exist"


@pytest.mark.django_db
def test_edit_task_with_invalid_payload(common_user_token):
    # Extract user and access token from fixture
    access_token = common_user_token.get("access")
    user = common_user_token.get("user")
    
    # Create API client and set authorization header
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    # Prepare task data
    name = f"{user.username}'s Task Name"
    description = f"{user.username}'s Task Description"
    task = Task.objects.create(name=name, description=description)
    
    # Prepare invalid payload for editing the task
    invalid_payload = {"name": "Updated Task Name"}
    
    # Prepare URL for editing the task
    url = reverse("edit-task", kwargs={"pk": task.id})
    
    # Make PUT request to edit the task with invalid payload
    response = client.put(url, data=invalid_payload, format="json")
    
    # Assert that the request returns a 400 error due to invalid payload
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
@pytest.mark.django_db
def test_edit_task_without_authentication(common_user_token):
    # Extract user from fixture
    user = common_user_token.get("user")
    
    # Create API client without setting authorization header
    client = APIClient()
    
    # Prepare task data
    name = f"{user.username}'s Task Name"
    description = f"{user.username}'s Task Description"
    task = Task.objects.create(name=name, description=description)
    
    # Prepare updated task data
    second_name = "Task Renamed"
    second_description = "Task Description edited"
    payload = {"name": second_name, "description": second_description}
    
    # Prepare URL for editing the task
    url = reverse("edit-task", kwargs={"pk": task.id})
    
    # Make PUT request to edit the task without authentication
    response = client.put(url, data=payload, format="json")
    
    # Assert that the request returns a 401 error due to lack of authentication
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
