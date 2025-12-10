from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=250)
    department = models.CharField(max_length=250)
    phone = models.CharField(max_length=16)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    