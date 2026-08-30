"""
patients/forms.py
Strong form validation using Django forms + custom clean methods
"""

from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from .models import Owner, Patient, Species


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            'address',
            'city',
            'notes',
            Submit('submit', 'Save Owner', css_class='btn btn-success')
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            qs = Owner.objects.filter(email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("An owner with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise ValidationError("Phone number is required.")
        return phone


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'owner', 'species', 'name', 'breed', 'gender',
            'date_of_birth', 'weight_kg', 'microchip_id', 'photo', 'notes', 'is_active'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('owner', css_class='col-md-6'),
                Column('species', css_class='col-md-6'),
            ),
            Row(
                Column('name', css_class='col-md-6'),
                Column('breed', css_class='col-md-6'),
            ),
            Row(
                Column('gender', css_class='col-md-4'),
                Column('date_of_birth', css_class='col-md-4'),
                Column('weight_kg', css_class='col-md-4'),
            ),
            Row(
                Column('microchip_id', css_class='col-md-6'),
                Column('photo', css_class='col-md-6'),
            ),
            'notes',
            'is_active',
            Submit('submit', 'Save Patient', css_class='btn btn-success')
        )
        self.fields['owner'].queryset = Owner.objects.all()
        self.fields['species'].queryset = Species.objects.all()

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise ValidationError("Pet name must be at least 2 characters.")
        return name.title()

    def clean_weight_kg(self):
        weight = self.cleaned_data.get('weight_kg')
        if weight is not None and weight <= 0:
            raise ValidationError("Weight must be greater than 0.")
        return weight
