# users/views.py
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, LoginForm
from .models import User

# Temporary in-memory storage for verification codes
verification_codes = {}

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # require verification
            user.save()
            code = random.randint(1000, 9999)
            verification_codes[user.username] = code
            print(f"Verification code for {user.username}: {code}")  # Console log
            return redirect('users:verify', username=user.username)
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})

def verify_view(request, username):
    if request.method == "POST":
        code = request.POST.get("code")
        if username in verification_codes and str(verification_codes[username]) == code:
            user = User.objects.get(username=username)
            user.is_active = True
            user.email_verified = True
            user.save()
            del verification_codes[username]
            return redirect("users:login")
    return render(request, "users/verify.html", {"username": username})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("users:dashboard")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})

@login_required
def dashboard_view(request):
    return render(request, "users/dashboard.html", {"user": request.user})

def logout_view(request):
    logout(request)
    return redirect("users:login")
