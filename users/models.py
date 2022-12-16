from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import AppUserManager
import uuid
from django.core.validators import MinLengthValidator

class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = AppUserManager()

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(AppUser, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=50, validators=[MinLengthValidator(5)])

    def __str__(self) -> str:
        return self.name

