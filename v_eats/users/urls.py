# users/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("register/", views.register_choice, name="register"),
    path("register/customer/", views.register_customer, name="register_customer"),
    path("register/restaurant/", views.register_restaurant, name="register_restaurant"),
    path("register/driver/", views.register_driver, name="register_driver"),
    path("verify/<int:user_id>/", views.verify_account, name="verify"),
    path("resend-verification/<int:user_id>/", views.resend_verification, name="resend_verification"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_view, name="logout"),
]
