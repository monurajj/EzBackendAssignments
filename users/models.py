from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ops', 'Operation User'),
        ('client', 'Client User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # Add unique related_name attributes
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Avoid conflict with auth.User
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Avoid conflict with auth.User
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
