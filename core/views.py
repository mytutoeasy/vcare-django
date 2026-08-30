"""
core/views.py
Dashboard + main pages
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q, F
from django.utils import timezone

from patients.models import Patient, PatientActivity
from appointments.models import Appointment
from inventory.models import InventoryItem


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        now = timezone.now()

        # KPI cards matching the UI design
        context['total_patients_today'] = (
            Appointment.objects.filter(scheduled_at__date=today)
            .exclude(status__in=['cancelled', 'no-show'])
            .values('patient')
            .distinct()
            .count()
        )

        context['upcoming_appointments'] = Appointment.objects.filter(
            scheduled_at__gt=now,
            status__in=['scheduled', 'confirmed']
        ).count()

        context['active_treatments'] = Appointment.objects.filter(
            status__in=['check-in', 'in-progress']
        ).count()

        context['inventory_alerts'] = InventoryItem.objects.filter(
            quantity__lte=F('reorder_level'),
            is_active=True,
            deleted_at__isnull=True
        ).count()

        # Today's appointments (calendar style)
        context['todays_appointments'] = (
            Appointment.objects.filter(scheduled_at__date=today)
            .select_related('patient', 'patient__species', 'type', 'veterinarian')
            .order_by('scheduled_at')
        )

        # Recent Patient Activity feed
        context['recent_activities'] = (
            PatientActivity.objects
            .select_related('patient', 'patient__species')
            .order_by('-occurred_at')[:8]
        )

        # Current Patients table
        context['current_patients'] = (
            Patient.objects.filter(is_active=True, deleted_at__isnull=True)
            .select_related('owner', 'species')
            .order_by('name')[:12]
        )

        context['today'] = today
        return context
