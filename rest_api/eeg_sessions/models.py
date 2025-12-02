from django.db import models
from scientists.models import Scientist
from patients.models import Patient
import uuid

class EEGSession(models.Model):
    SESSION_STATUS = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluída'),
        ('failed', 'Falha'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=100, unique=True, db_index=True)
    scientist = models.ForeignKey(
        Scientist,
        on_delete=models.CASCADE,
        related_name='eeg_sessions'
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='eeg_sessions',
        null=True,
        blank=True
    )
    
    edf_file_id = models.UUIDField(null=True, blank=True)
    trial_index = models.IntegerField(null=True, blank=True)
    start_time = models.FloatField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    emotion_category = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    parameters = models.JSONField(default=dict, blank=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=SESSION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'eeg_sessions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['edf_file_id']),
            models.Index(fields=['scientist', 'status']),
        ]

    def __str__(self):
        return f"EEG Session {self.session_id} - {self.scientist.scientist_id}"

    def save(self, *args, **kwargs):
        if not self.session_id:
            import random
            import string
            unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            self.session_id = f"eeg_{unique_id}"
        super().save(*args, **kwargs)