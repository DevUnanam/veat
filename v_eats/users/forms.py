# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, RestaurantProfile, DriverProfile

class BaseRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 dark:bg-gray-700 dark:text-white transition-colors duration-200'

        # Add placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone number'
        self.fields['address'].widget.attrs['placeholder'] = 'Your address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

class CustomerRegistrationForm(BaseRegistrationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role='USER',
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
        return user

class RestaurantRegistrationForm(BaseRegistrationForm):
    business_name = forms.CharField(max_length=200, required=True)
    business_license = forms.CharField(max_length=100, required=True)
    business_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    business_phone = forms.CharField(max_length=15, required=True)
    business_email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['business_name'].widget.attrs['placeholder'] = 'Your Restaurant Name'
        self.fields['business_license'].widget.attrs['placeholder'] = 'Business License Number'
        self.fields['business_address'].widget.attrs['placeholder'] = 'Restaurant Address'
        self.fields['business_phone'].widget.attrs['placeholder'] = 'Restaurant Phone'
        self.fields['business_email'].widget.attrs['placeholder'] = 'Restaurant Email'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            user_profile = UserProfile.objects.create(
                user=user,
                role='RESTAURANT',
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
            RestaurantProfile.objects.create(
                user=user,
                business_name=self.cleaned_data['business_name'],
                business_license=self.cleaned_data['business_license'],
                business_address=self.cleaned_data['business_address'],
                business_phone=self.cleaned_data['business_phone'],
                business_email=self.cleaned_data['business_email']
            )
        return user

class DriverRegistrationForm(BaseRegistrationForm):
    license_number = forms.CharField(max_length=50, required=True)
    vehicle_type = forms.ChoiceField(choices=DriverProfile.VEHICLE_TYPES, required=True)
    vehicle_plate = forms.CharField(max_length=20, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['license_number'].widget.attrs['placeholder'] = 'Driver License Number'
        self.fields['vehicle_plate'].widget.attrs['placeholder'] = 'Vehicle Plate Number'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            user_profile = UserProfile.objects.create(
                user=user,
                role='DRIVER',
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
            DriverProfile.objects.create(
                user=user,
                license_number=self.cleaned_data['license_number'],
                vehicle_type=self.cleaned_data['vehicle_type'],
                vehicle_plate=self.cleaned_data['vehicle_plate']
            )
        return user

class VerificationForm(forms.Form):
    verification_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 dark:bg-gray-700 dark:text-white transition-colors duration-200 text-center text-2xl tracking-widest',
            'placeholder': '000000',
            'maxlength': '6'
        })
    )
