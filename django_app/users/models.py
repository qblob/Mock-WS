from django.contrib.auth.models import User
from django.db import models


class UserLevel(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    photo = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    level = models.ForeignKey(
        UserLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    def __str__(self):
        return self.user.username