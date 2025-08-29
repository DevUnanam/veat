from django.contrib import admin
from .models import Restaurant, MenuItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'category', 'status', 'rating', 'created_at')
    list_filter = ('category', 'status', 'is_delivery_available', 'created_at')
    search_fields = ('name', 'description', 'owner__username', 'address')
    readonly_fields = ('created_at', 'updated_at', 'rating', 'total_reviews')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'owner', 'description', 'category', 'status')
        }),
        ('Contact & Location', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('Images', {
            'fields': ('image', 'logo')
        }),
        ('Operating Hours', {
            'fields': ('opening_time', 'closing_time')
        }),
        ('Delivery Settings', {
            'fields': ('is_delivery_available', 'delivery_fee', 'minimum_order')
        }),
        ('Statistics', {
            'fields': ('rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'is_available', 'is_vegetarian', 'is_vegan', 'restaurant__name')
    search_fields = ('name', 'description', 'restaurant__name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('restaurant', 'name', 'description', 'category', 'price')
        }),
        ('Options', {
            'fields': ('is_available', 'is_vegetarian', 'is_vegan', 'preparation_time')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
