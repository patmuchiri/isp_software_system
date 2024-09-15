from django.db import models
from django.contrib.auth.models import User

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    upload_speed = models.DecimalField(max_digits=5, decimal_places=2, help_text="Upload speed (Mbps)")  # Mbps
    download_speed = models.DecimalField(max_digits=5, decimal_places=2, help_text="Download speed (Mbps)")  # Mbps
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in local currency")  # Price in local currency

    def __str__(self):
        return f'{self.name} - {self.download_speed} Mbps down / {self.upload_speed} Mbps up'

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    static_ip = models.GenericIPAddressField(protocol='IPv4', unique=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.email})'

class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.client.name} - {self.start_date} to {self.end_date}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()

    def __str__(self):
        return self.full_name
