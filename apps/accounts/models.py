from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model. We start from Django's default fields (username,
    email, password, is_staff, etc.) and add what a shop customer needs.
    Using a custom User from day one means we can extend it later
    (e.g. loyalty points, saved addresses) without a painful migration.
    """
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="e.g. 2547XXXXXXXX - used for M-Pesa STK push and order updates",
    )

    def __str__(self):
        return self.username
