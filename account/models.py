from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.conf import settings



# Community Model
class Community(models.Model):
    community_name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.community_name


class UserProfileManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=128,unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=128, default=make_password(None))
    last_login = models.DateTimeField(blank=True, null=True)
    login_attempts = models.IntegerField(default=0)
    lastlogin_datetime = models.DateTimeField(blank=True, null=True)
    modify_datetime = models.DateTimeField(auto_now=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE,blank=True,null=True)
    is_community_owner=models.BooleanField(default=False)
    is_community_member=models.BooleanField(default=False)
    is_community_customer=models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_profiles',
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_profiles',
        blank=True
    )

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username


# Block Model
class Block(models.Model):
    block_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('block_name', 'community')

    def __str__(self):
        return f"{self.block_name} - {self.community}"

# Flat Model
class Flat(models.Model):
    flat_number = models.CharField(max_length=50)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)  # The owner/tenant
    meter_no = models.CharField(max_length=100, unique=True)

    class Meta:
        unique_together = ('flat_number', 'block')

    def __str__(self):
        return f"Flat {self.flat_number}, Block {self.block}, Community {self.community}" 
