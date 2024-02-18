import pytest

from rest_framework.test import APIClient
from rest_framework import status
from users.test.fixtures import common_user, common_user_token

from django.urls import reverse

from task.models import Task

# ===========================================
# ============== CREATE TASK ================
# ===========================================

@pytest.mark.django_db
def test_create_task_successfully(common_user_token):
    user = common_user_token.get("user")
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    user = common_user_token.get("user")
    name = f"{user.username}’s Task Name"
    description = f"{user.username}’s Task Description"
    payload = {"name": name, "description": description}
    url = reverse("create-task")
    response = client.post(url, data=payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    task_id = response.json().get("data").get("id")
    task = Task.objects.get(id=task_id)
    assert task.name == name
    assert task.description == description


@pytest.mark.django_db
def test_create_task_whit_repite_name(common_user_token):
    user = common_user_token.get("user")
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    name = f"{user.username}'s Task Name"
    description = f"{user.username}'s Task Description"
    task = Task.objects.create(name=name, description=description)
    
    second_name = "Task Renamed"
    payload = {"name": name, "description": description}
    url = reverse("create-task")
    response = client.post(url, data=payload, format="json")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    #we change the name and try again
    
    task.name = second_name
    task.save()
    second_response = client.post(url, data=payload, format="json")
    
    assert second_response.status_code == status.HTTP_200_OK
    
    second_task_id = second_response.json().get("data").get("id")
    second_task = Task.objects.get(id=second_task_id)
    assert second_task.name == name
    assert second_task.description == description

@pytest.mark.django_db
def test_create_task_with_invalid_payload(common_user_token):
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    invalid_payload = {"name": "Task Name"}
    
    url = reverse("create-task")
    response = client.post(url, data=invalid_payload, format="json")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
@pytest.mark.django_db
def test_create_task_without_authentication():
    client = APIClient()
    
    payload = {"name": "Task Name", "description": "Task Description"}
    
    url = reverse("create-task")
    response = client.post(url, data=payload, format="json")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
# ===========================================
# ============== DETAIL TASK ================
# ===========================================

@pytest.mark.django_db
def test_get_existing_task(common_user_token):
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    name = "Task Name"
    description = "Task Description"
    
    task = Task.objects.create(name=name, description=description)
    
    url = reverse("task", kwargs={"pk": task.id})
    
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    
    assert response.data.get("task").get("name") == name
    assert response.data.get("task").get("description") == description

@pytest.mark.django_db
def test_get_non_existing_task(common_user_token):
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    url = reverse("task", kwargs={"pk": 999})
    response = client.get(url)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data.get("error") == "Task does not exist"
    
@pytest.mark.django_db
def test_get_task_without_authentication():
    client = APIClient()
    
    name = "Task Name"
    description = "Task Description"
    
    task = Task.objects.create(name=name, description=description)
    
    url = reverse("task", kwargs={"pk": task.id})
    response = client.get(url)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# ===========================================
# ============== DELETE TASK ================
# ===========================================

@pytest.mark.django_db
def test_delete_task(common_user_token):
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    name = "Task Name"
    description = "Task Description"
    
    task = Task.objects.create(name=name, description=description)
    
    url = reverse("task", kwargs={"pk": task.id})
    response = client.delete(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("message") == "Task deleted"
    
    assert not Task.objects.filter(pk=task.pk, is_active=True).exists()

@pytest.mark.django_db
def test_delete_non_existing_task(common_user_token):
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    url = reverse("task", kwargs={"pk": 999})
    response = client.delete(url)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data.get("error") == "Task does not exist"
    
@pytest.mark.django_db
def test_delete_task_without_authentication():
    client = APIClient()
    
    name = "Task Name"
    description = "Task Description"
    
    task = Task.objects.create(name=name, description=description)
    
    url = reverse("task", kwargs={"pk": task.id})
    response = client.delete(url)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# ===========================================
# ============== TASK LIST ==================
# ===========================================

@pytest.mark.django_db
def test_get_task_list(common_user_token):
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    Task.objects.create(name="Task 1", description="Task Description 1")
    Task.objects.create(name="Task 2", description="Task Description 2")
    
    url = reverse("task-list")
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    
    tasks = response.data.get('tasks')
    
    assert len(tasks) == 2

@pytest.mark.django_db
def test_empty_task_list(common_user_token):
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    url = reverse("task-list")
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    
    tasks = response.data.get('tasks')
    
    assert len(tasks) == 0

@pytest.mark.django_db
def test_get_task_list_without_authentication():
    client = APIClient()
    
    Task.objects.create(name="Task 1", description="Task Description 1")
    Task.objects.create(name="Task 2", description="Task Description 2")
    
    url = reverse("task-list")
    response = client.get(url)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    

# ===========================================
# ============== EDIT TASK ==================
# ===========================================

@pytest.mark.django_db
def test_edit_task_successfully(common_user_token):
    user = common_user_token.get("user")
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    task = Task.objects.create(name="Task 1", description="Task Description 1")
    
    second_name = "Task Renamed"
    second_description = "Task Description edited"
    
    payload = {"name": second_name, "description": second_description}
    url = reverse("edit-task",kwargs={"pk": task.id})
    response = client.put(url, data=payload, format="json")
    
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_edit_non_existing_task(common_user_token):
    user = common_user_token.get("user")
    access_token = common_user_token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    name = f"{user.username}'s Task Name"
    description = f"{user.username}'s Task Description"
    
    payload = {"name": name, "description": description}
    
    url = reverse("edit-task", kwargs={"pk": 999}) 
    response = client.put(url, data=payload, format="json")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data.get("error") == "Task does not exist"


@pytest.mark.django_db
def test_edit_task_with_invalid_payload(common_user_token):
    access_token = common_user_token.get("access")
    user = common_user_token.get("user")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    
    name = f"{user.username}'s Task Name"
    description = f"{user.username}'s Task Description"
    
    task = Task.objects.create(name=name, description=description)
    
    invalid_payload = {"name": "Updated Task Name"}
    
    url = reverse("edit-task", kwargs={"pk": task.id})
    response = client.put(url, data=invalid_payload, format="json")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
@pytest.mark.django_db
def test_edit_task_without_authentication(common_user_token):
    user = common_user_token.get("user")
    client = APIClient()
    
    name = f"{user.username}'s Task Name"
    description = f"{user.username}'s Task Description"
    task = Task.objects.create(name=name, description=description)
    
    second_name = "Task Renamed"
    second_description = "Task Description edited"
    
    payload = {"name": second_name, "description": second_description}
    url = reverse("edit-task",kwargs={"pk": task.id})
    response = client.put(url, data=payload, format="json")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED