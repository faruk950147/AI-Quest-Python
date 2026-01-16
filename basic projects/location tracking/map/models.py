from django.db import models

class Number(models.Model):
    number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Number"
        verbose_name_plural = "Numbers"
