from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.utils.crypto import get_random_string
from scientists.models import Scientist
from django.core.exceptions import ValidationError
import uuid

class PatientManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)

        if 'patient_iid' not in extra_fields:
            name = extra_fields.get('first_name', '') + ' ' + extra_fields.get('last_name', '')
            name = name.strip() or email.split('@')[0]
            unique_salt = get_random_string(6)
            patient_iid = f"{name}_{unique_salt}"[:100]
            extra_fields['patient_iid'] = patient_iid

        extra_fields.setdefault('is_active', True)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class Patient(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_iid = models.CharField(max_length=100, unique=True, db_index=True)
    is_test = models.BooleanField(default=False)
    scientist = models.ForeignKey(Scientist, on_delete=models.CASCADE, related_name='patients', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    clinical_notes = models.TextField(null=True, blank=True)
    additional_info = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='Os grupos aos quais este usuário pertence. Um usuário receberá todas as permissões concedidas a cada um dos seus grupos.',
        related_name="patient_groups",
        related_query_name="patient",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Permissões específicas à esse usuário',
        related_name="patient_permissions",
        related_query_name="patient",
    )

    objects = PatientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'patient_metadata'

    def __str__(self):
        return f"{self.patient_iid} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.patient_iid:
            name = f"{self.first_name} {self.last_name}".strip() or self.email.split('@')[0]
            unique_salt = get_random_string(6)
            self.patient_iid = f"{name}_{unique_salt}"[:100]

        if Patient.objects.filter(patient_iid=self.patient_iid).exclude(id=self.id).exists():
            unique_salt = get_random_string(6)
            self.patient_iid = f"{self.patient_iid}_{unique_salt}"[:100]
        
        super().save(*args, **kwargs)