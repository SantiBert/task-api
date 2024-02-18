from django.db import transaction

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status

from .serializers import TaskSerializer, CrateTaskSerializer
from .models import Task

class GetTaskView(GenericAPIView):
    # Requires authentication for this view
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    
    def get(self, request, pk):
        try:
            # Get the task with the given ID
            task = Task.objects.get(id=pk, is_active=True)
            # Serialize the task
            serializer = TaskSerializer(task)
            # Return the serialized task in the response
            return Response({"task": serializer.data}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            # Task with the given ID doesn't exist
            return Response({"error": "Task does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Other exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        try:
            # Get the task with the given ID
            task = Task.objects.get(id=pk, is_active=True)
            # Mark the task as inactive
            task.is_active = False
            task.save()
            # Return success message
            return Response({"message": "Task deleted"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            # Task with the given ID doesn't exist
            return Response({"error": "Task does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Other exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskListView(GenericAPIView):
    # Requires authentication for this view
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    
    def get(self, request):
        try:
            # Get all active tasks
            tasks = Task.objects.filter(is_active=True)
            # Serialize the tasks
            serializer = TaskSerializer(tasks, many=True)
            # Return the serialized tasks in the response
            return Response({"tasks": serializer.data}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            # No active tasks found
            return Response({"error": "Task does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Other exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateTaskView(GenericAPIView):
    # Requires authentication for this view
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrateTaskSerializer
    
    @transaction.atomic()
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Invalid input data
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Create a new task
            name = serializer.validated_data["name"]
            description = serializer.validated_data["description"]
            task = Task.objects.create(name=name, description=description)
            # Serialize the created task
            result_serializer = TaskSerializer(task)
            # Return success message along with serialized task
            return Response({"message": "Task created", "data": result_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            # Other exceptions
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EditTaskView(GenericAPIView):
    # Requires authentication for this view
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrateTaskSerializer
    
    def put(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Invalid input data
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get the task with the given ID
            task = Task.objects.get(id=pk, is_active=True)
            # Update task details
            name = serializer.validated_data["name"]
            description = serializer.validated_data["description"]
            task.name = name
            task.description = description
            task.save()
            # Serialize the updated task
            result_serializer = TaskSerializer(task)
            # Return success message along with serialized task
            return Response({"message": "Task updated", "data": result_serializer.data}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            # Task with the given ID doesn't exist
            return Response({"error": "Task does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Other exceptions
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
