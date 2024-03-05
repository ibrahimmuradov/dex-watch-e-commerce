from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy
from services.uploader import Uploader
from services.mixin import DateMixin
from phonenumber_field.modelfields import PhoneNumberField


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, email, password, **other_fields)

    def create_user(self, username, email, password, **other_fields):
        if not email:
            raise ValueError(gettext_lazy('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()

        return user


class UserBase(AbstractUser, PermissionsMixin, DateMixin):
    email = models.EmailField(gettext_lazy('email_address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    mobile = PhoneNumberField(blank=True)
    profile_photo = models.ImageField(upload_to=Uploader.upload_profile_photo, default='../static/assets/img/default.png', max_length=500, blank=True)
    token_key = models.CharField(max_length=50, null=True, unique=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'settings.EMAIL_HOST_USER',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.username


class Address(DateMixin):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=270, blank=True)
    address = models.CharField(max_length=300)
    country = models.ForeignKey('order.Country', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=150)
    phone = PhoneNumberField()
    postal_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f'{self.user.username}'
