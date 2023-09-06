import datetime
from django.core.mail import EmailMessage,  get_connection
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from django.conf import settings


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    date_joined = models.DateField(default=datetime.datetime.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

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
            EmailMessage(subject, message, from_email, [self.email], connection=connection).send()
