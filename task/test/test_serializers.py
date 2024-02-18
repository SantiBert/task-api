import pytest
from task.models import Task
from task.serializers import TaskSerializer, CrateTaskSerializer

# Test the TaskSerializer class
@pytest.mark.django_db
def test_task_serializer():
    # Create a task object
    task = Task.objects.create(name="Task Name", description="Task Description")
    
    # Serialize the task object
    serializer = TaskSerializer(task)
    
    # Verify that the serialized data matches the task object's attributes
    assert serializer.data["id"] == task.id
    assert serializer.data["name"] == task.name
    assert serializer.data["description"] == task.description

# Test the CrateTaskSerializer class with valid data
def test_create_task_serializer_with_valid_data():
    # Valid data for creating a task
    valid_data = {"name": "Task Name", "description": "Task Description"}
    
    # Create a serializer instance with the valid data
    serializer = CrateTaskSerializer(data=valid_data)
    
    # Verify that the serializer is valid and that the required fields are present in the validated data
    assert serializer.is_valid() == True
    assert "name" in serializer.validated_data
    assert "description" in serializer.validated_data

# Test the CrateTaskSerializer class with invalid data
def test_create_task_serializer_with_invalid_data():
    # Invalid data for creating a task (missing 'name' field)
    invalid_data = {"description": "Task Description"}
    
    # Create a serializer instance with the invalid data
    serializer = CrateTaskSerializer(data=invalid_data)
    
    # Verify that the serializer is invalid and that the error is related to the missing 'name' field
    assert serializer.is_valid() == False
    assert "name" in serializer.errors
