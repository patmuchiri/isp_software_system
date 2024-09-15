from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
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

# Form for client registration and editing
class ClientRegistrationForm(forms.ModelForm):
    upload_speed = forms.DecimalField(max_digits=5, decimal_places=2, label="Upload Speed (Mbps)")
    download_speed = forms.DecimalField(max_digits=5, decimal_places=2, label="Download Speed (Mbps)")
    price = forms.DecimalField(max_digits=10, decimal_places=2, label="Price")

    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number', 'static_ip', 'start_date']

    def save(self, commit=True):
        client = super().save(commit=False)
        # Get or create subscription plan with specified speeds and price
        upload_speed = self.cleaned_data.get('upload_speed')
        download_speed = self.cleaned_data.get('download_speed')
        price = self.cleaned_data.get('price')

        subscription_plan, created = SubscriptionPlan.objects.get_or_create(
            name=f"{upload_speed} Mbps / {download_speed} Mbps",
            defaults={
                'upload_speed': upload_speed,
                'download_speed': download_speed,
                'price': price
            }
        )
        client.subscription_plan = subscription_plan

        if commit:
            client.save()
        return client

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
            return redirect('register_user')  # Redirect back to registration page with success parameter
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

@login_required
def view_users(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            user.delete()
            return redirect('view_users')

    users = User.objects.all()
    return render(request, 'view_users.html', {'users': users})

@login_required
def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client registered successfully.')
            return redirect('user_home')  # Redirect to user home
    else:
        form = ClientRegistrationForm()
    return render(request, 'register_client.html', {'form': form})

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

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client deleted successfully.')
        return redirect('user_home')
    return render(request, 'confirm_delete.html', {'client': client})

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def user_home(request):
    # Fetch all clients to display on the user home page
    clients = Client.objects.all()
    return render(request, 'user_home.html', {'clients': clients})

@login_required
def view_clients(request):
    clients = Client.objects.all()
    return render(request, 'view_clients.html', {'clients': clients})
