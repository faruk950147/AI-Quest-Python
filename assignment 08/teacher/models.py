from django.db import models
from collage.models import Collage, Department
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Teacher(models.Model):
    collage = models.ForeignKey(Collage, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length= 150)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=15)

  
    def __str__(self):
        return f"Name of teacher {self.name}"