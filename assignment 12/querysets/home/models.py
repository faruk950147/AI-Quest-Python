from django.db import models

# Create your models here.        
class Student(models.Model):
    name = models.CharField(max_length=200, unique=True)
    roll = models.IntegerField(default=101, unique=True)
    department = models.CharField(max_length=200)
    pased_in_years = models.IntegerField(default=0)
    pased_out_years = models.IntegerField(default=0)

    def __str__(self):
        return self.name