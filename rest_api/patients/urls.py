from django.urls import path
from . import views
from patients.views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.PatientCreateView.as_view(), name='patient-register'),
    path('test-register/', views.TestPatientCreateView.as_view(), name='patient-test-register'),
    path('complete-profile/', views.PatientProfileCompletionView.as_view(), name='patient-complete-profile'),
    path('check-eligibility/', views.check_session_eligibility, name='check-eligibility'),
    path('list/', views.PatientListView.as_view(), name='patient-list'),
    path('detail/<uuid:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('scientist-update/<uuid:pk>/', views.ScientistUpdatePatientView.as_view(), name='scientist-update-patient'),
    path('available/', AvailablePatientsListView.as_view(), name='available-patients'),
    path('link/<uuid:pk>/', LinkPatientToScientistView.as_view(), name='link-patient'),
]