from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from .forms import RegistrationForm, LoginForm
from .models import User


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            login(request, user)
            return redirect('accounts:dashboard_redirect')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:dashboard_redirect')
        return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('jobs:job_list')


@login_required
def dashboard_redirect(request):
    user: User = request.user
    if user.is_employer():
        return redirect('accounts:employer_dashboard')
    return redirect('accounts:applicant_dashboard')


class EmployerDashboardView(TemplateView):
    template_name = 'accounts/employer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ApplicantDashboardView(TemplateView):
    template_name = 'accounts/applicant_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

# Create your views here.
