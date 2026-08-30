from django.contrib import admin
from .models import Species, Owner, Patient, PatientActivity

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'city')
    search_fields = ('first_name', 'last_name', 'phone', 'email')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'owner', 'gender', 'is_active')
    list_filter = ('species', 'gender', 'is_active')
    search_fields = ('name', 'owner__first_name', 'owner__last_name', 'microchip_id')
    raw_id_fields = ('owner',)

@admin.register(PatientActivity)
class PatientActivityAdmin(admin.ModelAdmin):
    list_display = ('patient', 'title', 'status_tag', 'occurred_at')
    list_filter = ('activity_type',)
