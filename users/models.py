from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import AppUserManager

class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_join = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = AppUserManager()