# QuantumLapis · Job Portal (Django 4)

A professional job portal where Employers post jobs and Applicants search and apply. Built with Django 4, SQLite, and Bootstrap.
<img width="1268" height="812" alt="image" src="https://github.com/user-attachments/assets/2316fec6-e8ac-4466-ba77-de9d360fccd7" />

## Features
- Role-based auth with a custom `User` model (`employer` / `applicant`)
- Job posting and management for employers
- Job search by title, company, and location with pagination
- Applications with resume upload and cover letter
- Dashboards for both roles
- Admin registration for all models
- Seed script for demo data

## Tech Stack
- Python 3.11+
- Django 4.2
- SQLite (default)
- Bootstrap 5, Font Awesome

## Getting Started
These commands assume Windows PowerShell from the project root.

```powershell
# 1) Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2) Install dependencies
python -m pip install --upgrade pip
pip install django==4.2.14

# 3) Run migrations
python manage.py migrate

# 4) Create demo data (users, 55+ jobs, and applications)
python manage.py seed_job_portal --count 50

# 5) Start the dev server
python manage.py runserver
```

Open http://localhost:8000

## Demo Accounts
- Employer: `employer_demo` / `password123`
- Applicant: `applicant_demo` / `password123`

Optional admin:
```powershell
python manage.py createsuperuser
```

## Project Structure
```
job_portal/
├── accounts/              # Custom user, auth views
├── jobs/                  # Job and application models, views, seed command
├── templates/             # HTML templates (Bootstrap based)
├── static/                # CSS, images (QuantumLapis logo)
├── job_portal/            # Settings, urls
└── manage.py
```

## Key URLs
- Home / Job list: `/`
- Job detail: `/job/<id>/`
- Post job (Employer): `/post/`
- My jobs (Employer): `/my-jobs/`
- Apply (Applicant): `/job/<id>/apply/`
- Applicants list (Employer): `/job/<id>/applicants/`
- Auth: `/accounts/login/`, `/accounts/register/`, `/accounts/logout/`
- Dashboards: `/accounts/dashboard/` (auto-redirects by role)
- Admin: `/admin/`

## File Uploads
Resumes are stored under `media/resumes/`. In development, media is served automatically when `DEBUG=True`.

## Environment / Settings
- Static files: `static/`
- Media files: `media/`
- Custom user: `AUTH_USER_MODEL = 'accounts.User'`

## Notes
- The UI uses a light, professional theme with a one-time splash intro. To see the intro again, open the site in a new browser session or clear site data for the domain.
- For a production deployment, configure a proper database, static/media hosting, environment variables, and a WSGI/ASGI server.

## License
This project is provided as-is for demonstration and educational purposes.
