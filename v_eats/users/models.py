# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import random
import string

class UserProfile(models.Model):
    USER_ROLES = [
        ('SUPERUSER', 'Super User'),
        ('RESTAURANT', 'Restaurant Owner'),
        ('USER', 'Customer'),
        ('DRIVER', 'Delivery Driver'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=15, choices=USER_ROLES, default='USER')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    def generate_verification_code(self):
        """Generate a 6-digit verification code"""
        self.verification_code = ''.join(random.choices(string.digits, k=6))
        self.save()
        return self.verification_code

    def verify_code(self, code):
        """Verify the provided code"""
        if self.verification_code == code:
            self.is_verified = True
            self.verification_code = None
            self.save()
            return True
        return False

class RestaurantProfile(models.Model):
    APPROVAL_STATUS = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('SUSPENDED', 'Suspended'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant_profile')
    business_name = models.CharField(max_length=200)
    business_license = models.CharField(max_length=100, unique=True)
    business_address = models.TextField()
    business_phone = models.CharField(max_length=15)
    business_email = models.EmailField()
    status = models.CharField(max_length=15, choices=APPROVAL_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} - {self.status}"

class DriverProfile(models.Model):
    APPROVAL_STATUS = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('SUSPENDED', 'Suspended'),
    ]

    VEHICLE_TYPES = [
        ('BIKE', 'Motorcycle'),
        ('CAR', 'Car'),
        ('BICYCLE', 'Bicycle'),
        ('SCOOTER', 'Scooter'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    vehicle_plate = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=15, choices=APPROVAL_STATUS, default='PENDING')
    rating = models.FloatField(default=0.0)
    total_deliveries = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle_type} Driver"
