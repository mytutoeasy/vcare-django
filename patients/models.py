"""
patients/models.py
Owners, Species, Patients + Activity feed
Strong validation + soft delete pattern
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])


class Species(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji for UI")

    class Meta:
        verbose_name_plural = 'Species'
        ordering = ['name']

    def __str__(self):
        return self.name


class Owner(SoftDeleteModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Enter a valid phone number (e.g. +1234567890)"
            )
        ]
    )
    address = models.TextField(blank=True)
    city = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        if self.email:
            self.email = self.email.lower().strip()


class Patient(SoftDeleteModel):
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        UNKNOWN = 'unknown', 'Unknown'

    owner = models.ForeignKey(
        Owner,
        on_delete=models.PROTECT,
        related_name='pets'
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.PROTECT,
        related_name='patients'
    )
    name = models.CharField(max_length=80)
    breed = models.CharField(max_length=80, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.UNKNOWN
    )
    date_of_birth = models.DateField(null=True, blank=True)
    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.1), MaxValueValidator(500)]
    )
    microchip_id = models.CharField(
        max_length=50,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9\-]+$',
                message="Microchip ID can only contain letters, numbers and hyphens."
            )
        ]
    )
    photo = models.ImageField(upload_to='patients/', blank=True, null=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.species.name})"

    def clean(self):
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError({'date_of_birth': 'Date of birth cannot be in the future.'})

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class PatientActivity(models.Model):
    """
    Used for the "Recent Patient Activity" widget on the dashboard
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities'
    )
    activity_type = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    status_tag = models.CharField(
        max_length=30,
        blank=True,
        help_text="UI pill text: Check-up, Surgery, Vaccination..."
    )
    occurred_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Patient activities'
        ordering = ['-occurred_at']
        indexes = [
            models.Index(fields=['-occurred_at']),
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.title}"
