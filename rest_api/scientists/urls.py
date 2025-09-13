from django.urls import path
from .views import ScientistCreateView, ScientistProfileView, verify_scientists

urlpatterns = [
    path('register/', ScientistCreateView.as_view(), name='scientist-register'),
    path('profile/', ScientistProfileView.as_view(), name='scientist-profile'),
    path('verify/<str:token>/', verify_scientists, name='verify-scientist'),
]