from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        if extra_fields.get("is_superuser") is True:
            raise ValueError(_("User cannot be a Superuser"))
        if extra_fields.get("user_type") == "superuser":
            raise ValueError(_("User type cannot be a Superuser"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", "superuser")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("Superuser must have is_active=True"))

        return self.create_user(email, password, **extra_fields)
