from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from random import choice, randint, sample
from accounts.models import User
from jobs.models import Job, Application


class Command(BaseCommand):
    help = 'Seed the database with demo users, jobs, and applications'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of extra random jobs to create')

    def handle(self, *args, **options):
        employer, _ = User.objects.get_or_create(
            username='employer_demo', defaults={'role': User.ROLE_EMPLOYER, 'email': 'employer@example.com'}
        )
        employer.set_password('password123')
        employer.role = User.ROLE_EMPLOYER
        employer.save()

        applicant, _ = User.objects.get_or_create(
            username='applicant_demo', defaults={'role': User.ROLE_APPLICANT, 'email': 'applicant@example.com'}
        )
        applicant.set_password('password123')
        applicant.role = User.ROLE_APPLICANT
        applicant.save()

        jobs_data = [
            {
                'title': 'Senior Backend Engineer',
                'company_name': 'BlueWave Tech',
                'location': 'Remote',
                'description': 'Design and build scalable APIs with Django and PostgreSQL. Work with a friendly remote team.',
            },
            {
                'title': 'Frontend Developer',
                'company_name': 'PixelCraft Studios',
                'location': 'Lagos, NG',
                'description': 'Build delightful UIs with React and TypeScript. Collaborate with designers and product managers.',
            },
            {
                'title': 'Data Analyst',
                'company_name': 'Insightify',
                'location': 'Nairobi, KE',
                'description': 'Turn raw data into insights. SQL, Python, and visualization experience required.',
            },
            {
                'title': 'DevOps Engineer',
                'company_name': 'CloudNest',
                'location': 'Hybrid - Accra, GH',
                'description': 'Automate CI/CD pipelines and manage cloud infrastructure. Docker, Kubernetes a plus.',
            },
            {
                'title': 'Product Manager',
                'company_name': 'Nova Labs',
                'location': 'Remote - EMEA',
                'description': 'Own the roadmap, work with cross-functional teams, and ship great products.',
            },
        ]

        created_jobs = []
        for jd in jobs_data:
            job, _ = Job.objects.get_or_create(
                title=jd['title'],
                company_name=jd['company_name'],
                defaults={
                    'location': jd['location'],
                    'description': jd['description'],
                    'posted_by': employer,
                    'created_at': timezone.now(),
                },
            )
            created_jobs.append(job)

        # Random sets for generating more jobs
        titles = [
            'Software Engineer', 'Mobile Developer', 'QA Engineer', 'ML Engineer',
            'SRE', 'UX Designer', 'Systems Analyst', 'Solutions Architect', 'Tech Lead', 'Support Engineer'
        ]
        companies = [
            'ApexWorks', 'NextGen Soft', 'Brightly', 'Orbital Systems', 'Nimbus Corp',
            'Starlight Labs', 'Quantum Peak', 'Aurora Apps', 'Zenith Tech', 'Helixware'
        ]
        locations = ['Remote', 'Lagos, NG', 'Abuja, NG', 'Nairobi, KE', 'Kampala, UG', 'Accra, GH', 'Cairo, EG', 'Cape Town, ZA']

        extra_count = max(0, int(options.get('count') or 0))
        for _ in range(extra_count):
            jd = {
                'title': choice(titles),
                'company_name': choice(companies),
                'location': choice(locations),
                'description': 'We are looking for a passionate professional to join our growing team. '
                               'Responsibilities include collaboration, implementation, and continuous improvement.',
            }
            job = Job.objects.create(
                title=jd['title'],
                company_name=jd['company_name'],
                location=jd['location'],
                description=jd['description'],
                posted_by=employer,
                created_at=timezone.now() - timezone.timedelta(days=randint(0, 60)),
            )
            created_jobs.append(job)

        # Create multiple applicant users and random applications
        applicants: list[User] = [applicant]
        for i in range(1, 6):
            u, _ = User.objects.get_or_create(
                username=f'applicant_demo_{i}', defaults={'role': User.ROLE_APPLICANT, 'email': f'applicant{i}@example.com'}
            )
            u.set_password('password123')
            u.role = User.ROLE_APPLICANT
            u.save()
            applicants.append(u)

        # Each applicant applies to 2-4 random jobs
        for u in applicants:
            for job in sample(created_jobs, k=min(len(created_jobs), randint(2, 4))):
                app, created = Application.objects.get_or_create(job=job, applicant=u)
                if created or not app.resume:
                    resume_bytes = (f"Resume for {u.username}\nSkills: Python, Django, SQL, Git\n").encode()
                    resume_content = ContentFile(resume_bytes)
                    resume_content.name = 'resume.txt'
                    app.cover_letter = 'I am excited to apply and contribute to your team.'
                    app.resume.save('resume.txt', resume_content, save=False)
                    app.save()

        self.stdout.write(self.style.SUCCESS(f'Seeded demo users, {len(created_jobs)} jobs, and applications.'))

