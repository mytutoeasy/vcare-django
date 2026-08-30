# 🐾 vCare – Veterinary Care System (Django)

A progressive Django project that grows from **beginner** to **advanced**, matching the white/green dashboard UI.

## Features already included

- Custom User model with roles (Veterinarian, Nurse, Receptionist…)
- Full models: Owners, Patients, Species, Appointments, Medical Records, Inventory, Activity feed
- Strong form validation + model validators
- Soft-delete pattern
- Bootstrap 5 + custom green/white theme (matching the UI mockup)
- Crispy Forms for beautiful forms
- Dashboard with live KPIs
- Django Admin fully configured
- Ready for MySQL (commented config)

---

## 1. Beginner Setup (5 minutes)

```bash
cd vcare_project
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install django pillow django-crispy-forms crispy-bootstrap5
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and login.

---

## 2. Intermediate – Add sample data

```bash
python manage.py shell
```

```python
from patients.models import Species, Owner, Patient
from accounts.models import User

# Species
Species.objects.bulk_create([
    Species(name='Dog', icon='🐕'),
    Species(name='Cat', icon='🐈'),
    Species(name='Rabbit', icon='🐇'),
    Species(name='Bird', icon='🐦'),
])

# Owner + Patient example
owner = Owner.objects.create(
    first_name='James', last_name='Wilson',
    phone='+15551234567', email='james@example.com'
)
Patient.objects.create(
    owner=owner,
    species=Species.objects.get(name='Dog'),
    name='Buddy', breed='Golden Retriever', gender='male'
)
```

---

## 3. Advanced – Switch to MySQL

1. Install MySQL client:
   ```bash
   pip install mysqlclient
   ```
2. Create database:
   ```sql
   CREATE DATABASE vcare_db CHARACTER SET utf8mb4;
   ```
3. Uncomment the MySQL block in `settings.py` and fill credentials.
4. Run `python manage.py migrate`

---

## Project Structure

```
vcare_project/
├── accounts/          # Custom User + auth
├── core/              # Dashboard + ClinicSettings
├── patients/          # Owners, Patients, Activity
├── appointments/      # Appointments + Medical Records
├── inventory/         # Stock + low-stock alerts
├── templates/         # Bootstrap 5 templates
├── static/css/        # Custom green theme
└── manage.py
```

---

## Next steps you can add (advanced)

- [ ] Appointment calendar with FullCalendar.js
- [ ] Django REST Framework API
- [ ] Celery + Redis for reminders
- [ ] PDF medical reports (WeasyPrint)
- [ ] Role-based permissions (django-guardian)
- [ ] Unit tests + coverage
- [ ] Docker + docker-compose
- [ ] CI/CD with GitHub Actions

---

Made with ❤️ for veterinary clinics.
