from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    department = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Student(models.Model):

    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science'),
        ('EEE', 'Electrical Engineering'),
        ('BBA', 'Business Administration'),
    ]

    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    roll = models.PositiveIntegerField(unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    passed_in_year = models.DateField()
    passed_out_year = models.DateField()

    def __str__(self):
        return f"{self.roll} - {self.name}"

    class Meta:
        ordering = ['roll']