from django.db import models
from django.utils import timezone
from user_auth.models.custom_user import CustomUser


class BlackList(models.Model):
    token = models.CharField(max_length=50)
    custom_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tokens")
    date_blacklisted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.custom_user.email
