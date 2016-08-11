from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)


class Role(models.Model):
    role_name = models.CharField(
        max_length=255,
        unique=True)
    display_name = models.CharField(
        max_length=255,
        unique=True)

    def __str__(self):
        return self.display_name


class AppUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True)
    first_name = models.CharField(
        max_length=255)
    last_name = models.CharField(
        max_length=255,
        blank=True)
    sex = models.CharField(
        max_length=1,
        blank=True)
    date_of_birth = models.DateField(
        blank=True,
        null=True)
    phone_number = models.CharField(
        max_length=20,
        blank=True)
    address_line_1 = models.CharField(
        max_length=255,
        blank=True)
    address_line_2 = models.CharField(
        max_length=255,
        blank=True)
    city = models.CharField(
        max_length=255,
        blank=True)
    state = models.CharField(
        max_length=255,
        blank=True)
    postal_code = models.CharField(
        max_length=255,
        blank=True)
    country = models.CharField(
        max_length=255,
        blank=True)
    image = models.ImageField(upload_to='customers/profile_pictures', blank=True)
    roles = models.ManyToManyField(
        Role,
        related_name='role_appuser',
        blank=True)
    is_active = models.BooleanField(
        default=True)
    is_admin = models.BooleanField(
        default=False)
    is_verified = models.BooleanField(
        default=False)
    added_on = models.DateTimeField(
        auto_now_add=True)
    updated_on = models.DateTimeField(
        auto_now=True)
    reset_password_token = models.CharField(
        max_length=8,
        blank=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True,
        null=True, related_name='updated_by_user')

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    ALREADY_EXISTS = 'The user already exists'

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, *args, **kwargs):
        return True

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'User'