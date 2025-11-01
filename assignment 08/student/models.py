from django.db import models
from collage.models import Collage, Department
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Student(models.Model):
    collage = models.ForeignKey(Collage, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length= 150)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=15)
    cgpa = models.DecimalField(validators=[ MinValueValidator(3.50), MaxValueValidator(5.00)], max_digits=5, decimal_places=2)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return f"Name of student {self.name}"