from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Restaurant(models.Model):
    CATEGORY_CHOICES = [
        ('fast_food', 'Fast Food'),
        ('casual', 'Casual Dining'),
        ('fine_dining', 'Fine Dining'),
        ('cafe', 'Cafe'),
        ('bakery', 'Bakery'),
        ('dessert', 'Dessert'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending Approval'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_restaurants')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_delivery_available = models.BooleanField(default=True)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    minimum_order = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant:detail', kwargs={'pk': self.pk})

    def get_dashboard_url(self):
        return reverse('restaurant:dashboard', kwargs={'pk': self.pk})

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
        ('side', 'Side Dish'),
        ('special', 'Special'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    preparation_time = models.IntegerField(help_text="Time in minutes", default=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"
