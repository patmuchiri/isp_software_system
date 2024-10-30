from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from .models import Client, SubscriptionPlan
from .mikrotik_api import MikroTikAPI
from .forms import ClientRegistrationForm
from django.core.mail import send_mail
from django_otp.models import Device
from django.contrib.auth.decorators import login_required
import pyotp

# MikroTik credentials
MIKROTIK_IP = '102.215.32.180'
MIKROTIK_USERNAME = 'pat'
MIKROTIK_PASSWORD = '#@phenom@2024'

# User Registration Form
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

# Client Registration Form
class ClientRegistrationForm(forms.ModelForm):
    upload_speed = forms.DecimalField(max_digits=5, decimal_places=2, label="Upload Speed (Mbps)")
    download_speed = forms.DecimalField(max_digits=5, decimal_places=2, label="Download Speed (Mbps)")
    price = forms.DecimalField(max_digits=10, decimal_places=2, label="Price")

    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number', 'static_ip', 'start_date']

    def save(self, commit=True):
        client = super().save(commit=False)
        upload_speed = self.cleaned_data.get('upload_speed')
        download_speed = self.cleaned_data.get('download_speed')
        price = self.cleaned_data.get('price')

        # Ensure the Subscription Plan exists or create it
        subscription_plan, created = SubscriptionPlan.objects.get_or_create(
            name=f"{upload_speed} Mbps / {download_speed} Mbps",
            defaults={'upload_speed': upload_speed, 'download_speed': download_speed, 'price': price}
        )
        client.subscription_plan = subscription_plan

        if commit:
            client.save()

            # Activate client in MikroTik
            api = MikroTikAPI(host=MIKROTIK_IP, username=MIKROTIK_USERNAME, password=MIKROTIK_PASSWORD)
            api.add_queue(client.static_ip, upload_speed, download_speed)

        return client

# Landing Page
def landing(request):
    return render(request, 'landing.html')

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard' if user.is_superuser else 'user_home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

# User Registration
@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User registered successfully.')
            return redirect('register_user')
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

# View Users (Admin only)
@login_required
def view_users(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            User.objects.get(id=user_id).delete()
            messages.success(request, 'User deleted successfully.')
            return redirect('view_users')

    users = User.objects.all()
    return render(request, 'view_users.html', {'users': users})

# Client Registration
@login_required
def register_client(request):
    if request.method == 'POST':
        print (request.POST)
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client registered successfully.')
            return redirect('admin_dashboard' if request.user.is_superuser else 'user_home')
    else:
        form = ClientRegistrationForm()
    return render(request, 'register_client.html', {'form': form})

# Edit Client
@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client details updated successfully.')
            return redirect('user_home')
    else:
        form = ClientRegistrationForm(instance=client)
    return render(request, 'edit_client.html', {'form': form})

# Delete Client
@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        # Remove client from MikroTik
        api = MikroTikAPI(host="102.215.32.180", username="pat", password="#@phenom2024")
        api.remove_queue(client.static_ip)
        client.delete()
        messages.success(request, 'Client deleted successfully.')
        return redirect('user_home')
    return render(request, 'confirm_delete.html', {'client': client})

# Admin Dashboard
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# User Home Dashboard
@login_required
def user_home(request):
    clients = Client.objects.all()
    return render(request, 'user_home.html', {'clients': clients})

# View Clients
@login_required
def view_clients(request):
    clients = Client.objects.all()
    return render(request, 'view_clients.html', {'clients': clients})

@login_required
def send_otp(request):
    user = request.user
    device = Device.objects.get_or_create(user=user)[0]
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  # 5 minutes validity
    device.generate_challenge()
    send_mail(
        'Your OTP for email verification',
        f'Your OTP is: {totp.now()}',  # Send OTP via email
        'your_email@example.com',
        [user.email],
        fail_silently=False,
    )
    return redirect('verify_otp')

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = request.user
        device = Device.objects.get(user=user)
        if device.verify_token(otp):
            return redirect('home')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'verify_otp.html')
