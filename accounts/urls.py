from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/employer/', views.EmployerDashboardView.as_view(), name='employer_dashboard'),
    path('dashboard/applicant/', views.ApplicantDashboardView.as_view(), name='applicant_dashboard'),
]

