from django.contrib import admin
from .models import AppointmentType, Appointment, MedicalRecord

@admin.register(AppointmentType)
class AppointmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'duration_minutes')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'veterinarian', 'type', 'scheduled_at', 'status')
    list_filter = ('status', 'type', 'scheduled_at')
    search_fields = ('patient__name', 'veterinarian__username')
    date_hierarchy = 'scheduled_at'
    raw_id_fields = ('patient', 'veterinarian')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'record_type', 'title', 'veterinarian', 'recorded_at')
    list_filter = ('record_type',)
