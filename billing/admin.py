from django.contrib import admin
from .models import Client, SubscriptionPlan, Subscription

admin.site.register(Client)
admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
