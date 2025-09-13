from django.urls import path
from .views import PatientLoginViewJWT, ScientistLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/patients/', PatientLoginViewJWT.as_view(), name='patient-login'),
    path('login/scientists/', ScientistLoginView.as_view(), name='scientist-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]