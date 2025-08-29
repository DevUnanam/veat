# users/views.py
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomerRegistrationForm, RestaurantRegistrationForm, DriverRegistrationForm, VerificationForm
from .models import User, UserProfile
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Home page view"""
    return render(request, 'users/home.html')

def register_choice(request):
    """Let users choose their registration type"""
    return render(request, 'users/register_choice.html')

def register_customer(request):
    """Customer registration view"""
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Generate verification code
                verification_code = user.profile.generate_verification_code()

                # Log to console (in production, send via SMS/Email)
                print(f"Verification code for {user.username}: {verification_code}")
                logger.info(f"Verification code for {user.username}: {verification_code}")

                messages.success(request, 'Registration successful! Check your console for verification code.')
                return redirect('users:verify', user_id=user.id)
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                logger.error(f"Registration error: {str(e)}")
        else:
            # Form is not valid, show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'users/register_customer.html', {'form': form})

def register_restaurant(request):
    """Restaurant registration view"""
    if request.method == 'POST':
        form = RestaurantRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Generate verification code
            verification_code = user.profile.generate_verification_code()

            # Log to console (in production, send via SMS/Email)
            print(f"Verification code for {user.username}: {verification_code}")
            logger.info(f"Verification code for {user.username}: {verification_code}")

            messages.success(request, 'Restaurant registration successful! Check your console for verification code.')
            return redirect('users:verify', user_id=user.id)
    else:
        form = RestaurantRegistrationForm()

    return render(request, 'users/register_restaurant.html', {'form': form})

def register_driver(request):
    """Driver registration view"""
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Generate verification code
            verification_code = user.profile.generate_verification_code()

            # Log to console (in production, send via SMS/Email)
            print(f"Verification code for {user.username}: {verification_code}")
            logger.info(f"Verification code for {user.username}: {verification_code}")

            messages.success(request, 'Driver registration successful! Check your console for verification code.')
            return redirect('users:verify', user_id=user.id)
    else:
        form = DriverRegistrationForm()

    return render(request, 'users/register_driver.html', {'form': form})

def verify_account(request, user_id):
    """Account verification view"""
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('users:register_choice')

    if user_profile.is_verified:
        messages.info(request, 'Account already verified.')
        return redirect('users:login')

    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['verification_code']
            if user_profile.verify_code(code):
                login(request, user_profile.user)
                messages.success(request, 'Account verified successfully!')

                # Redirect based on user role
                if user_profile.role == 'RESTAURANT':
                    return redirect('restaurant:dashboard')
                elif user_profile.role == 'DRIVER':
                    return redirect('driver:dashboard')
                else:
                    return redirect('users:home')
            else:
                messages.error(request, 'Invalid verification code.')
    else:
        form = VerificationForm()

    return render(request, 'users/verify.html', {
        'form': form,
        'user_profile': user_profile
    })

def resend_verification(request, user_id):
    """Resend verification code"""
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
        verification_code = user_profile.generate_verification_code()

        # Log to console (in production, send via SMS/Email)
        print(f"New verification code for {user_profile.user.username}: {verification_code}")
        logger.info(f"New verification code for {user_profile.user.username}: {verification_code}")

        return JsonResponse({'success': True, 'message': 'Verification code sent! Check console.'})
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found.'})

@login_required
def dashboard(request):
    """Role-based dashboard redirect"""
    user_profile = request.user.profile

    if user_profile.role == 'SUPERUSER':
        return redirect('admin:dashboard')
    elif user_profile.role == 'RESTAURANT':
        return redirect('restaurant:dashboard')
    elif user_profile.role == 'DRIVER':
        return redirect('driver:dashboard')
    else:
        return redirect('customer:dashboard')

@login_required
def profile(request):
    """User profile view"""
    return render(request, 'users/profile.html')

def logout_view(request):
    """Custom logout view that handles GET requests"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:home')
