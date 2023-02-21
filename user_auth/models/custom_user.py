from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import datetime, timedelta
from .custom_user_manager import CustomUserManager
import jwt


class CustomUser(AbstractBaseUser, PermissionsMixin):

    USER_CHOICE = (
        ("customer", "customer"),
        ("supplier", "supplier"),
        ("staff", "staff")
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=13)
    street = models.CharField(
        max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(
        max_length=30)
    zip_code = models.CharField(
        max_length=30)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    user_type = models.CharField(
        max_length=20, choices=USER_CHOICE, default="customer")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    @property
    def token(self):
        token = jwt.encode({"full_name": self.full_name(), "email": self.email,
                            "exp": datetime.utcnow() + timedelta(hours=1)}, settings.SECRET_KEY, algorithm="HS256")
        return token
