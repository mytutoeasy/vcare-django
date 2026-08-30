from .models import ClinicSettings


def clinic_status(request):
    try:
        settings = ClinicSettings.load()
        return {
            'clinic_name': settings.clinic_name,
            'clinic_is_live': settings.is_live,
        }
    except Exception:
        return {
            'clinic_name': 'vCare',
            'clinic_is_live': True,
        }
