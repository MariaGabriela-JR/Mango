from django.contrib.auth.backends import BaseBackend
from scientists.models import Scientist
from patients.models import Patient
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('user_id')
            user_type = validated_token.get('user_type')
            
            if user_type == 'scientist':
                return Scientist.objects.get(pk=user_id)
            elif user_type == 'patient':
                return Patient.objects.get(pk=user_id)
            else:
                raise AuthenticationFailed('User type invalid on token')
                
        except Scientist.DoesNotExist:
            raise AuthenticationFailed('Scientist not found')
        except Patient.DoesNotExist:
            raise AuthenticationFailed('Patient not found')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication error: {str(e)}')

class UniversalAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            patient = Patient.objects.get(email=email)
            if patient.check_password(password):
                return patient
        except Patient.DoesNotExist:
            pass
        
        try:
            scientist = Scientist.objects.get(email=email)
            if scientist.check_password(password):
                return scientist
        except Scientist.DoesNotExist:
            return None
        
        return None

    def get_user(self, user_id):
        if not user_id:
            return None
        
        try:
            try:
                return Scientist.objects.get(pk=user_id)
            except Scientist.DoesNotExist:
                pass

            try:
                return Patient.objects.get(pk=user_id)
            except Patient.DoesNotExist:
                return None
            
        except (ValueError, TypeError):
            return None
        except Exception as e:
            print(f"Error in get_user: {e}")
            return None
        
class PatientBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            patient = Patient.objects.get(email=email)
            if patient.check_password(password):
                return patient
        except Patient.DoesNotExist:
            return None

class ScientistBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            scientist = Scientist.objects.get(email=email)
            if scientist.check_password(password):
                return scientist
        except Scientist.DoesNotExist:
            return None