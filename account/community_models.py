from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


from django.db import models
from django.conf import settings

# Community Model
class Community(models.Model):
    community_name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)  # Latitude of the community
    longitude = models.FloatField(blank=True, null=True)  # Longitude of the community
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="community_created_user",
        blank=True,
        null=True,
    )
    modified_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="community_modified_user",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.community_name




# Block Model
class Block(models.Model):
    block_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="block_created_user",
        blank=True,
        null=True,
    )
    modified_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="block_modified_user",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('block_name', 'community')

    def __str__(self):
        return f"{self.block_name} - {self.community}"


# Flat Model
class Flat(models.Model):
    flat_number = models.CharField(max_length=50)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="flats")
    meter_no = models.CharField(max_length=100, unique=True)
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="flat_created_user",
        blank=True,
        null=True,
    )
    modified_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="flat_modified_user",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('flat_number', 'block')

    def __str__(self):
        return f"Flat {self.flat_number}, Block {self.block}, Community {self.community}"