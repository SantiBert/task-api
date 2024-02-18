import pytest
from task.models import Task
from task.serializers import TaskSerializer, CrateTaskSerializer

@pytest.mark.django_db
def test_task_serializer():
    task = Task.objects.create(name="Task Name", description="Task Description")
    
    serializer = TaskSerializer(task)
    
    assert serializer.data["id"] == task.id
    assert serializer.data["name"] == task.name
    assert serializer.data["description"] == task.description
    assert serializer.data["date_created"] == task.date_created.isoformat()

def test_create_task_serializer_with_valid_data():
    
    valid_data = {"name": "Task Name", "description": "Task Description"}
    
    serializer = CrateTaskSerializer(data=valid_data)
    
    assert serializer.is_valid() == True
    assert "name" in serializer.validated_data
    assert "description" in serializer.validated_data

def test_create_task_serializer_with_invalid_data():

    invalid_data = {"description": "Task Description"}
    
    serializer = CrateTaskSerializer(data=invalid_data)
    
    assert serializer.is_valid() == False
    assert "name" in serializer.errors
