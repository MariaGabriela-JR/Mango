from django.urls import path
from .views import PatientLoginViewJWT, ScientistLoginView, MeView, LogoutView, UserUpdateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/patients/', PatientLoginViewJWT.as_view(), name='patient-login'),
    path('login/scientists/', ScientistLoginView.as_view(), name='scientist-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path("users/update/", UserUpdateView.as_view(), name="user-update"),
    path('me/', MeView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout')
]