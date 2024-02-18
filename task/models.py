from django.utils import timezone
from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=250,unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    date_crated = models.DateTimeField(default=timezone.now, blank=True)
    
    class Meta:
       ordering = ["-date_crated"]
    
    def __str__(self):
        return self.name