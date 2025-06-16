from django.db import models


class UserOTP(models.Model):
    username = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.mobile}"
