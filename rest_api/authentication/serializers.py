from rest_framework import serializers
from django.contrib.auth import authenticate
from scientists.models import Scientist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class PatientLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )

            if not user:
                msg = 'Credenciais inválidas'
                raise serializers.ValidationError(msg, code='authorization')
            
            if not user.is_active:
                msg = 'Conta desativada'
                raise serializers.ValidationError(msg, code='authorization')
            
            from patients.models import Patient
            if not isinstance(user, Patient):
                msg = 'Usuário não é um paciente'
                raise serializers.ValidationError(msg, code='authorization')
            
            self.user = user
        
        data = super().validate(attrs)
        
        data.update({
            'id': self.user.id,
            'patient_iid': self.user.patient_iid,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'is_active': self.user.is_active,
            'is_staff': self.user.is_staff
        })
        
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['patient_iid'] = user.patient_iid
        token['user_type'] = 'patient'
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        return token
    
class ScientistLoginSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not user or not hasattr(user, "scientist_id"):
            msg = "Usuário e/ou senha incorreto(s) ou não é um cientista"
            raise serializers.ValidationError(msg, code="authorization")

        refresh = self.get_token(user)


        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_type": "scientist",
            "id": user.id,
            "scientist_id": user.scientist_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "institution": user.institution,
            "specialization": user.specialization,
            "is_verified": user.is_verified,
            "is_active": user.is_active,
        }

        return data
        
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = 'scientist'
        token['scientist_id'] = user.scientist_id
        token['institution'] = user.institution
        token['is_verified'] = user.is_verified
        return token