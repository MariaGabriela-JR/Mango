from rest_framework import serializers
from .models import Patient
from scientists.models import Scientist
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import date
from dateutil.relativedelta import relativedelta

class PatientSerializer(serializers.ModelSerializer):
    scientist = serializers.PrimaryKeyRelatedField(
        queryset=Scientist.objects.all(),
        required=False,
        allow_null=True
    )
    age = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'patient_iid': {'read_only': True},
            'groups': {'read_only': True},
            'user_permissions': {'read_only': True},
            'is_active': {'read_only': True},
            'is_test': {'read_only': True},
            'cpf': {'required': True},
            'email': {'required': False},
        }

    
    def validate_password(self, value):
        if not value or len(value) < 8:
            raise serializers.ValidationError("The password must have 8 digits")
        return value

    def validate_birth_date(self, value):
        """Date of birth validation"""
        if value:
            if value > date.today():
                raise serializers.ValidationError("Birth date can't be in the future.")
            age = relativedelta(date.today(), value).years
            if age < 1:
                raise serializers.ValidationError("Patient must have at least 1 year old")
            if age > 120:
                raise serializers.ValidationError("Invalid birth date")
        return value

    def validate_cpf(self, value):
        """Basic CPF validation"""
        if value:
            cpf_clean = ''.join(filter(str.isdigit, value))
            if len(cpf_clean) != 11:
                raise serializers.ValidationError("CPF must have 11 digits")
            if Patient.objects.filter(cpf=cpf_clean).exists():
                raise serializers.ValidationError("CPF already registered")
        return value

    def create(self, validated_data):
        if 'cpf' in validated_data:
            validated_data['cpf'] = ''.join(filter(str.isdigit, validated_data['cpf']))
        
        groups_data = validated_data.pop('groups', [])
        user_permissions_data = validated_data.pop('user_permissions', [])

        password = validated_data.pop('password', None)
        validated_data['is_active'] = True

        scientist = self.context.get('scientist', None)
        if scientist:
            validated_data['scientist'] = scientist
        
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        
        instance.save()

        if groups_data:
            instance.groups.set(groups_data)
        if user_permissions_data:
            instance.user_permissions.set(user_permissions_data)
        
        return instance
    
    def update(self, instance, validated_data):
        if 'cpf' in validated_data:
            validated_data['cpf'] = ''.join(filter(str.isdigit, validated_data['cpf']))
        
        groups_data = validated_data.pop('groups', None)
        user_permissions_data = validated_data.pop('user_permissions', None)

        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
            
        instance.save()

        if groups_data is not None:
            instance.groups.set(groups_data)
        if user_permissions_data is not None:
            instance.user_permissions.set(user_permissions_data)

        return instance

class PatientCPFLoginSerializer(TokenObtainPairSerializer):
    """Serializer for login with CPF"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(required=True)
        self.fields['password'] = serializers.CharField(required=True)

    def validate(self, attrs):
        cpf = ''.join(filter(str.isdigit, attrs.get('cpf', '')))
        attrs['cpf'] = cpf
        
        authenticate_kwargs = {
            self.username_field: cpf,
            'password': attrs['password']
        }
        
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None or not self.user.is_active:
            raise serializers.ValidationError('CPF or password is incorrect')

        data = {}
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data