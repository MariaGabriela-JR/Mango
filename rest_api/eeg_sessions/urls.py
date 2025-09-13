from django.urls import path
from . import views

urlpatterns = [
    path('', views.EEGSessionListView.as_view(), name='eeg-sessions-list'),
    path('create/', views.EEGSessionCreateView.as_view(), name='eeg-sessions-create'),
    path('<uuid:pk>/', views.EEGSessionDetailView.as_view(), name='eeg-sessions-detail'),
    path('<uuid:pk>/delete/', views.EEGSessionDetailView.as_view(), name='eeg-sessions-delete'),
    path('<uuid:pk>/update-data/', views.EEGSessionUpdateDataView.as_view(), name='eeg-sessions-update-data'),
    path('<uuid:pk>/sync-fastapi/', views.EEGSessionSyncFastAPIView.as_view(), name='eeg-sessions-sync-fastapi'),
    path('<uuid:pk>/change-status/', views.EEGSessionChangeStatusView.as_view(), name='eeg-sessions-change-status'),
    path('by-patient/<uuid:patient_id>/', views.EEGSessionByPatientView.as_view(), name='eeg-sessions-by-patient'),
    path('by-status/<str:status>/', views.EEGSessionByStatusView.as_view(), name='eeg-sessions-by-status'),
]