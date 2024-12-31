from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,Permission
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from account.community_models import Community



# UserProfile Manager
class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user=self.create_user(email, password, **extra_fields)
        if user.is_superuser:
            all_permissions = Permission.objects.all()
            user.user_permissions.set(all_permissions)
        return user


# UserProfile Model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=128, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=128, default=make_password(None))
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        permissions = [
            ("add_user_group", "Can add User to Group"),
            ("delete_user_group", "Can delete the User Group"),
            ("add_user_permissions", "Can add the User permissions"),
            ("get_user_permissions", "Can get the User permissions"),
        ]


