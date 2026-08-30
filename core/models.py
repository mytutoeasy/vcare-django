"""
core/models.py
Clinic settings + helpers
"""

from django.db import models


class ClinicSettings(models.Model):
    clinic_name = models.CharField(max_length=100, default='vCare')
    logo = models.ImageField(upload_to='clinic/', blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')
    is_live = models.BooleanField(default=True, help_text="Show Live Clinic Status badge")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Clinic settings'

    def __str__(self):
        return self.clinic_name

    def save(self, *args, **kwargs):
        # Ensure only one instance
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
