from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Collage(models.Model):
    name = models.CharField(validators=[UnicodeUsernameValidator], max_length=200)
    state = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Name of collage {self.name}"
class Department(models.Model):
    collage = models.ForeignKey(Collage, on_delete=models.CASCADE, related_name='collages')
    name = models.CharField(validators=[UnicodeUsernameValidator], max_length=200)
    seat = models.IntegerField(default=1, validators=[MinValueValidator(5), MaxValueValidator(120)])
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=650000)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return f"Name of department {self.name}"