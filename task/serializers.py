from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name","description","date_crated"]
        
class CrateTaskSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    description = serializers.CharField()