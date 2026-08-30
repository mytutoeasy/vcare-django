from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Patient, Owner
from .forms import PatientForm, OwnerForm


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('owner', 'species').filter(is_active=True)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(owner__first_name__icontains=q) |
                Q(owner__last_name__icontains=q) |
                Q(breed__icontains=q)
            )
        return qs


class PatientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patients:list')
    success_message = "Patient was created successfully."


class PatientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patients:list')
    success_message = "Patient updated successfully."


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'

    def get_queryset(self):
        return super().get_queryset().select_related('owner', 'species')


class OwnerListView(LoginRequiredMixin, ListView):
    model = Owner
    template_name = 'patients/owner_list.html'
    context_object_name = 'owners'
    paginate_by = 20


class OwnerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'patients/owner_form.html'
    success_url = reverse_lazy('patients:owner_list')
    success_message = "Owner created successfully."
