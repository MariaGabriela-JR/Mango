from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from scientists.models import Scientist
from patients.models import Patient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class PatientLoginSerializer(TokenObtainPairSerializer):
    username_field = "cpf"
    cpf = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        cpf = attrs.get('cpf')
        password = attrs.get('password')

        if not cpf or not password:
            raise AuthenticationFailed('CPF and password are obligatory.')

        try:
            user = Patient.objects.get(cpf=cpf)
        except Patient.DoesNotExist:
            raise AuthenticationFailed('CPF or password incorrect.')

        if not user.check_password(password):
            raise AuthenticationFailed('CPF or password incorrect.')

        if not user.is_active:
            raise AuthenticationFailed('Deactivated account, enter in contact with support.')

        self.user = user
        data = super().validate(attrs)

        data.update({
            'id': self.user.id,
            'patient_iid': self.user.patient_iid,
            'cpf': self.user.cpf,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'is_active': self.user.is_active,
            'is_staff': self.user.is_staff,
            'user_type': 'patient',
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
            raise AuthenticationFailed("User and/or password are incorrect or user is not a scientist.")

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
        token['user_id'] = str(user.id)
        return token

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use")
        return value

    def validate_password(self, value):
        if value and len(value) < 8:
            raise serializers.ValidationError("The password must have 8 digits")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance