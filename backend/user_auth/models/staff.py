from django.db import models
from user_auth.models.custom_user import CustomUser
from order.models.store import Store


class Staff(models.Model):

    STANDARD = 'STD'
    MANAGER = 'MGR'
    SR_MANAGER = 'SRMGR'
    PRESIDENT = 'PRES'

    EMPLOYEE_TYPES = (
        (STANDARD, 'base employee'),
        (MANAGER, 'manager'),
        (SR_MANAGER, 'senior manager'),
        (PRESIDENT, 'president')
    )

    role = models.CharField(
        max_length=25, choices=EMPLOYEE_TYPES, default=STANDARD)
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=30)
    custom_user = models.OneToOneField(
        CustomUser, unique=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE,  related_name="staff")
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, blank=True, null=True, related_name="staff")

    class META:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.custom_user.first_name} {self.custom_user.last_name}"

    def full_name(self):
        return f"{self.custom_user.first_name} {self.custom_user.last_name}"
