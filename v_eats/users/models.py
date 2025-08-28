# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superuser', 'Superuser'),
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('restaurant', 'Restaurant'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
