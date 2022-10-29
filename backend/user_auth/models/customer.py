from django.db import models
from .custom_user import CustomUser


class Customer(models.Model):
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=30)
    custom_user = models.OneToOneField(
        CustomUser, unique=True, related_name="customer", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.custom_user.first_name} {self.custom_user.last_name}"

    def full_name(self):
        return f"{self.custom_user.first_name} {self.custom_user.last_name}"
