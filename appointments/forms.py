from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from accounts.models import User
from patients.models import Patient
from .models import Appointment, AppointmentType, MedicalRecord


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'patient', 'veterinarian', 'type', 'scheduled_at',
            'status', 'reason', 'notes'
        ]
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='col-md-6'),
                Column('veterinarian', css_class='col-md-6'),
            ),
            Row(
                Column('type', css_class='col-md-6'),
                Column('scheduled_at', css_class='col-md-6'),
            ),
            Row(
                Column('status', css_class='col-md-6'),
                Column('reason', css_class='col-md-6'),
            ),
            'notes',
            Submit('submit', 'Save Appointment', css_class='btn btn-success')
        )
        self.fields['veterinarian'].queryset = User.objects.filter(
            role=User.Role.VETERINARIAN, is_active=True
        )
        self.fields['patient'].queryset = Patient.objects.filter(is_active=True)

    def clean_scheduled_at(self):
        scheduled = self.cleaned_data.get('scheduled_at')
        if scheduled and scheduled < timezone.now() - timezone.timedelta(minutes=30):
            if not self.instance.pk:
                raise ValidationError("Cannot create an appointment too far in the past.")
        return scheduled

    def clean(self):
        cleaned = super().clean()
        patient = cleaned.get('patient')
        scheduled = cleaned.get('scheduled_at')
        vet = cleaned.get('veterinarian')

        if patient and scheduled and vet:
            conflict = Appointment.objects.filter(
                veterinarian=vet,
                scheduled_at__range=(
                    scheduled - timezone.timedelta(minutes=20),
                    scheduled + timezone.timedelta(minutes=20)
                ),
                status__in=['scheduled', 'confirmed', 'check-in', 'in-progress']
            )
            if self.instance.pk:
                conflict = conflict.exclude(pk=self.instance.pk)
            if conflict.exists():
                raise ValidationError(
                    "This veterinarian already has an appointment around this time."
                )
        return cleaned


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            'patient', 'appointment', 'veterinarian', 'record_type',
            'title', 'diagnosis', 'treatment', 'prescription', 'notes', 'recorded_at'
        ]
        widgets = {
            'recorded_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'diagnosis': forms.Textarea(attrs={'rows': 2}),
            'treatment': forms.Textarea(attrs={'rows': 2}),
            'prescription': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('patient', css_class='col-md-6'),
                Column('veterinarian', css_class='col-md-6'),
            ),
            Row(
                Column('appointment', css_class='col-md-6'),
                Column('record_type', css_class='col-md-6'),
            ),
            'title',
            'diagnosis',
            'treatment',
            'prescription',
            'notes',
            'recorded_at',
            Submit('submit', 'Save Medical Record', css_class='btn btn-success')
        )
