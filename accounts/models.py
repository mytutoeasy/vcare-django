"""
accounts/models.py
Custom User model with roles for vCare
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom user for staff members (vets, nurses, receptionists...)
    """
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        VETERINARIAN = 'veterinarian', 'Veterinarian'
        NURSE = 'nurse', 'Nurse'
        RECEPTIONIST = 'receptionist', 'Receptionist'
        STAFF = 'staff', 'Staff'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF,
        help_text="Staff role in the clinic"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"Dr. {self.get_full_name()}" if self.role == self.Role.VETERINARIAN else self.get_full_name()

    @property
    def full_name(self):
        return self.get_full_name() or self.username
