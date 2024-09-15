from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from billing.models import Client, Subscription, SubscriptionPlan  # Import your models

class Command(BaseCommand):
    help = 'Setup the Staff group with appropriate permissions'

    def handle(self, *args, **kwargs):
        # Create or get the Staff group
        staff_group, created = Group.objects.get_or_create(name='Staff')

        # Define the permissions to add
        permissions = [
            'view_client',
            'add_client',
            'change_client',
            'delete_client',
            'view_subscription',
            'add_subscription',
            'change_subscription',
            'delete_subscription',
            'view_subscriptionplan',
            'add_subscriptionplan',
            'change_subscriptionplan',
            'delete_subscriptionplan',
        ]

        for perm_codename in permissions:
            model_name = perm_codename.split('_')[1]  # Extract model name from permission code
            content_type = ContentType.objects.get_for_model(
                Client if model_name == 'client' else
                Subscription if model_name == 'subscription' else
                SubscriptionPlan
            )
            try:
                permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
                staff_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Permission "{perm_codename}" does not exist.'))

        self.stdout.write(self.style.SUCCESS('Staff group setup with permissions successfully.'))
