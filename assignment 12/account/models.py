from django.db import models
from django.contrib.auth.models import User

DIVISION_CHOICES = (
    ('Dhaka', 'Dhaka'),
    ('Rangpur', 'Rangpur'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Barishal', 'Barishal'),
    ('Chattogram', 'Chattogram'),
    ('Mymensingh', 'Mymensingh'),
    ('Sylhet', 'Sylhet'),
)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=200)
    division = models.CharField(choices=DIVISION_CHOICES, max_length=50)
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=100)
    villorroad = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, default='+880')
    zipcode = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.name} - {self.user.username}"
