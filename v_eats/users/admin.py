from django.contrib import admin
from .models import UserProfile, RestaurantProfile, DriverProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'is_verified', 'date_joined')
    list_filter = ('role', 'is_verified', 'date_joined')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('date_joined',)

@admin.register(RestaurantProfile)
class RestaurantProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'status', 'business_phone', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('business_name', 'user__username', 'business_license')
    readonly_fields = ('created_at',)

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle_type', 'license_number', 'status', 'is_available', 'rating')
    list_filter = ('vehicle_type', 'status', 'is_available')
    search_fields = ('user__username', 'license_number', 'vehicle_plate')
    readonly_fields = ('created_at', 'total_deliveries')
