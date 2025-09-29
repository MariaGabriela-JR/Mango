from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.crypto import get_random_string
from datetime import date
import uuid

class ScientistManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)
        
class Scientist(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scientist_id = models.CharField(max_length=100, unique=True, db_index=True)
    gender = models.CharField(max_length=20, choices=[("male", "male"), ("female", "female"), ("other", "other")], null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField( upload_to="scientists/profile_pictures/", null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    institution = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ScientistManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='Os grupos aos quais este usuário pertence.',
        related_name="scientist_groups",
        related_query_name="scientist",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Permissões específicas à esse usuário',
        related_name="scientist_permissions",
        related_query_name="scientist",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'institution', 'specialization']

    def __str__(self):
        return f"{self.scientist_id} ({self.email})"
    
    def save(self, *args, **kwargs):
        if not self.scientist_id:
            name = f"{self.first_name} {self.last_name}".strip()
            unique_salt = get_random_string(6)
            self.scientist_id = f"scientist_{name}_{unique_salt}"[:100]

        if Scientist.objects.filter(scientist_id=self.scientist_id).exclude(id=self.id).exists():
            unique_salt = get_random_string(6)
            self.scientist_id = f"{self.scientist_id}_{unique_salt}"[:100]
        
        super().save(*args, **kwargs)
        
    @property
    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        age = today.year - self.birth_date.year
        # Ajusta caso o aniversário ainda não tenha ocorrido este ano
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age