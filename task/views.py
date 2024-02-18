from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView, DestroyAPIView, GenericAPIView

from .serializer import TaskSerializer, CrateTaskSerializer
from .models import Task

class GetTaskView(GenericAPIView):
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = None
    
    def get(self, request, pk):
        try:
            task = Task.objects.get(id=pk,is_active=True)
            serializer = TaskSerializer(task)
            return Response({"task": serializer.data}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "Task does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        try:
            task = Task.objects.get(id=pk,is_active=True)
            task.is_active = False
            task.save()
            
            return Response({"message": "Task deleted"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "Task does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskListView(ListAPIView):
    queryset = Task.objects.filter(is_active= True)
    serializer_class = TaskSerializer

class CreateTaskView(GenericAPIView):
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrateTaskSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            name = serializer.validated_data["name"]
            description = serializer.validated_data["description"]
            
            task = Task.objects.create(
                name=name,
                description=description
            )
            result_serializer = TaskSerializer(task)
            return Response(
                {
                    "message": "Task created",
                    "data": result_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EditTaskView(GenericAPIView):
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrateTaskSerializer
    
    def put(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            task = Task.objects.get(id=pk,is_active=True)
            
            name = serializer.validated_data["name"]
            description = serializer.validated_data["description"]
            
            task.name = name
            task.description = description
            task.save()
            
            result_serializer = TaskSerializer(task)
            return Response(
                {
                    "message": "Task updated",
                    "data": result_serializer.data,
                },
                status=200,
            )
        except Task.DoesNotExist:
            return Response({"error": "Task does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)