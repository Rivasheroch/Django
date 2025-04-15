from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('advanced_user', 'Advanced User'),
        ('normal_user', 'Normal User'),
    ]
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='normal_user')
    is_approved = models.BooleanField(default=False)
