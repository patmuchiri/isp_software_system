from django.contrib import admin
from .models import Client, SubscriptionPlan, Subscription, UserProfile

admin.site.register(SubscriptionPlan)
admin.site.register(Client)
admin.site.register(Subscription)
admin.site.register(UserProfile)
