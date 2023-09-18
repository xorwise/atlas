import datetime

from django.utils import timezone

from .models import User, SubscriptionPayment
from django.conf import settings
from celery import shared_task


@shared_task
def check_subscriptions():
    users = User.objects.all().filter(last_payment__gt=datetime.date.today() - datetime.timedelta(days=31), 
                                      last_payment__lt=datetime.date.today() - datetime.timedelta(days=30))
    counter = 0
    for user in users:
        if user.balance >= settings.SUBSCRIPTION_PRICE and user.payment_active:
            new_payment = SubscriptionPayment(user=user)
            new_payment.save()
            user.is_paid = True
            user.balance -= settings.SUBSCRIPTION_PRICE
            user.last_payment = timezone.now()
        else:
            user.is_paid = False
            user.payment_active = False
        counter += 1
        user.save()
    print(f'{counter} users checked!')