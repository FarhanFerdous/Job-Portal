from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
from django.core.paginator import Paginator
from .models import Job, Application
from .forms import JobForm, ApplicationForm


class JobListView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        jobs = Job.objects.all().order_by('-created_at')
        if query:
            jobs = jobs.filter(
                Q(title__icontains=query) | Q(company_name__icontains=query) | Q(location__icontains=query)
            )
        paginator = Paginator(jobs, 10)
        page = request.GET.get('page')
        jobs_page = paginator.get_page(page)
        return render(request, 'jobs/job_list.html', {'jobs': jobs_page, 'query': query})


class JobDetailView(View):
    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        return render(request, 'jobs/job_detail.html', {'job': job})


@login_required
def post_job(request):
    if not request.user.is_employer():
        return redirect('accounts:dashboard_redirect')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job: Job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('jobs:my_jobs')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})


@login_required
def my_jobs(request):
    if not request.user.is_employer():
        return redirect('accounts:dashboard_redirect')
    jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})


@login_required
def apply_job(request, pk):
    if not request.user.is_applicant():
        return redirect('accounts:dashboard_redirect')
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application: Application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('accounts:applicant_dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@login_required
def job_applicants(request, pk):
    if not request.user.is_employer():
        return redirect('accounts:dashboard_redirect')
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    applications = job.applications.select_related('applicant').order_by('-applied_at')
    return render(request, 'jobs/job_applicants.html', {'job': job, 'applications': applications})

# Create your views here.
