from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.RestaurantListView.as_view(), name='list'),
    path('add/', views.add_restaurant, name='add'),
    path('my-restaurants/', views.my_restaurants, name='my_restaurants'),
    path('<int:pk>/dashboard/', views.restaurant_dashboard, name='dashboard'),
    path('<int:pk>/menu/', views.manage_menu, name='manage_menu'),
    path('<int:pk>/menu/add/', views.add_menu_item, name='add_menu_item'),
]
