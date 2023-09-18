from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


def add_my_login_form(request):
    return {
        'login_form': AuthenticationForm(),
    }


def settings_processor(request):
    public_id = settings.CLOUD_PAYMENTS_PUBLIC_ID 
    subscription_price = settings.SUBSCRIPTION_PRICE
    return {'public_id': public_id, 'subscription_price': subscription_price}