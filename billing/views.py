from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Client, SubscriptionPlan, Subscription
from django.contrib import messages

# Form for user registration
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

# Form for client registration
class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number', 'static_ip', 'subscription_plan', 'start_date']

def landing(request):
    return render(request, 'landing.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:  # Redirect admin to admin dashboard
                return redirect('admin_dashboard')
            else:  # Redirect regular users to user home
                return redirect('user_home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User registered successfully.')
            return redirect('admin_dashboard')  # Redirect to admin dashboard
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

@login_required
def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client registered successfully.')
            return redirect('admin_dashboard')  # Redirect to admin dashboard
    else:
        form = ClientRegistrationForm()
    return render(request, 'register_client.html', {'form': form})

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def view_clients(request):
    clients = Client.objects.all()
    return render(request, 'view_clients.html', {'clients': clients})
