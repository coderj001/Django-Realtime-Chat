from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse

from account.manager import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        max_length=60
    )
    username = models.CharField(
        max_length=50,
        unique=True
    )
    date_joined = models.DateTimeField(
        verbose_name='Date Jointed',
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        verbose_name='Last Login',
        auto_now=True
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Stuff Status'
    )
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(
        max_length=255,
        upload_to='profile/',
        null=True,
        blank=True,
        default='default_profile_image.png'
    )
    hide_email = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse(
            "account:account_view",
            kwargs={'id': self.id, }
        )
