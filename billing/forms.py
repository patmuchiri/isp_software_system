from django import forms
from .models import Client, SubscriptionPlan

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

        subscription_plan, created = SubscriptionPlan.objects.get_or_create(
            name=f"{upload_speed} Mbps / {download_speed} Mbps",
            defaults={'upload_speed': upload_speed, 'download_speed': download_speed, 'price': price}
        )
        client.subscription_plan = subscription_plan

        if commit:
            client.save()

            # Activate client in MikroTik (assuming MikroTikAPI exists)
            from .mikrotik_api import MikroTikAPI
            api = MikroTikAPI(host="102.215.32.180", username="pat", password="#@phenom2024")
            api.add_queue(client.static_ip, upload_speed, download_speed)

        return client

