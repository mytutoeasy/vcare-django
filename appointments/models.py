"""
appointments/models.py
Appointment types + Appointments + Medical Records
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User
from patients.models import Patient, SoftDeleteModel


class AppointmentType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(
        max_length=7,
        default='#4CAF50',
        help_text="Hex color for UI pills (e.g. #4CAF50)"
    )
    duration_minutes = models.PositiveSmallIntegerField(default=30)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Appointment(SoftDeleteModel):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        CONFIRMED = 'confirmed', 'Confirmed'
        CHECK_IN = 'check-in', 'Check-in'
        IN_PROGRESS = 'in-progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        NO_SHOW = 'no-show', 'No Show'

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    veterinarian = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='appointments',
        limit_choices_to={'role': 'veterinarian'}
    )
    type = models.ForeignKey(
        AppointmentType,
        on_delete=models.PROTECT,
        related_name='appointments'
    )
    scheduled_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )
    reason = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_appointments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_at']
        indexes = [
            models.Index(fields=['scheduled_at']),
            models.Index(fields=['status']),
            models.Index(fields=['veterinarian', 'scheduled_at']),
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.scheduled_at:%Y-%m-%d %H:%M} ({self.status})"

    def clean(self):
        if self.scheduled_at and self.scheduled_at < timezone.now() - timezone.timedelta(hours=1):
            if not self.pk:
                raise ValidationError({'scheduled_at': 'Cannot schedule an appointment in the past.'})

        if self.end_at and self.scheduled_at and self.end_at <= self.scheduled_at:
            raise ValidationError({'end_at': 'End time must be after start time.'})

    def save(self, *args, **kwargs):
        if not self.end_at and self.type_id:
            self.end_at = self.scheduled_at + timezone.timedelta(minutes=self.type.duration_minutes)
        super().save(*args, **kwargs)


class MedicalRecord(SoftDeleteModel):
    class RecordType(models.TextChoices):
        EXAMINATION = 'examination', 'Examination'
        SURGERY = 'surgery', 'Surgery'
        VACCINATION = 'vaccination', 'Vaccination'
        TREATMENT = 'treatment', 'Treatment'
        PRESCRIPTION = 'prescription', 'Prescription'
        LAB = 'lab', 'Lab'
        OTHER = 'other', 'Other'

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medical_records'
    )
    veterinarian = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='medical_records'
    )
    record_type = models.CharField(
        max_length=20,
        choices=RecordType.choices,
        default=RecordType.EXAMINATION
    )
    title = models.CharField(max_length=150)
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['patient', '-recorded_at']),
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.title}"
