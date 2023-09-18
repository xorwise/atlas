import datetime
from django.core.mail import EmailMessage,  get_connection
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

from .managers import UserManager
from django.conf import settings
import secrets
import string
from random import randint


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    date_joined = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    balance = models.FloatField(default=0)
    payment_active = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    last_payment = models.DateTimeField(default=timezone.now() - datetime.timedelta(days=40))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def email_user(self, subject: str, message: str, from_email: str = None, **kwargs):
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD
        ) as connection:
            print('test')
            resp = EmailMessage(subject, message, from_email, [self.email], connection=connection).send()
            print(resp)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    preview_image = models.ImageField(blank=True, null=True)
    boto3_id = models.UUIDField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_opened = models.DateTimeField(default=timezone.now)
    last_location = models.CharField(blank=True, null=True)


class BookMark(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    location = models.CharField()


class SubscriptionPayment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Deposit(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(blank=False, null=False)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)