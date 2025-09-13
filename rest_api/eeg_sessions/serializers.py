from rest_framework import serializers
from patients.views import Patient
from .models import EEGSession

class EEGSessionSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        required=False,
        allow_null=True
    )

    def to_internal_value(self, data):
        if 'patient' in data and data['patient'] == "":
            data['patient'] = None
        
        return super().to_internal_value(data)

    def validate_patient(self, value):
        if value and not Patient.objects.filter(
            id=value.id, 
            scientist=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(
                "Paciente não encontrado ou não pertence a você."
            )
        return value

    class Meta:
        model = EEGSession
        fields = '__all__'
        read_only_fields = ['session_id', 'created_at', 'updated_at', 'scientist']

class EEGSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EEGSession
        fields = [
            'patient', 'title', 'description', 'edf_file_id', 'trial_index',
            'start_time', 'duration', 'emotion_category', 'parameters'
        ]

class EEGSessionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EEGSession
        fields = [
            'status', 'edf_file_id', 'trial_index', 'start_time', 'duration',
            'emotion_category', 'description', 'parameters', 'title'
        ]