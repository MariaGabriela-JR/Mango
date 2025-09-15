from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .models import Patient, Scientist
from .serializers import PatientSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .fastapi_sync import sync_patient_to_fastapi

class ScientistIDMixin:
    def get_scientist(self):
        if isinstance(self.request.user, Scientist):
            return self.request.user

        scientist_id = self.request.headers.get('X-Scientist-ID') or self.request.query_params.get('scientist_id')
        if not scientist_id:
            raise PermissionDenied('Scientist ID é obrigatório')

        try:
            return Scientist.objects.get(id=scientist_id)
        except Scientist.DoesNotExist:
            try:
                return Scientist.objects.get(scientist_id=scientist_id)
            except Scientist.DoesNotExist:
                raise PermissionDenied('Cientista não encontrado')

class TestPatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['is_active'] = True
        data['is_test'] = True
        data['scientist'] = None

        for field in ['age', 'gender', 'clinical_notes', 'additional_info', 'groups', 'user_permissions', 'is_test']:
            data.pop(field, None)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        patient_dict = {
            "patient_iid": patient.patient_iid,
            "age": patient.age,
            "gender": patient.gender,
            "clinical_notes": patient.clinical_notes,
            "additional_info": patient.additional_info,
            "created_at": patient.created_at.isoformat(),
            "updated_at": patient.updated_at.isoformat(),
        }
        sync_patient_to_fastapi(patient_dict)

        response_data = serializer.data
        response_data.pop('password', None)
        return Response(response_data, status=status.HTTP_201_CREATED)


class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['is_active'] = True
        data['is_test'] = False

        for field in ['groups', 'user_permissions', 'is_test']:
            data.pop(field, None)

        scientist_id = data.get('scientist')
        if scientist_id:
            try:
                scientist = Scientist.objects.get(id=scientist_id)
                data['scientist'] = scientist.id
            except Scientist.DoesNotExist:
                return Response({'error': 'Cientista não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'error': 'ID do cientista inválido'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['scientist'] = None

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        patient_dict = {
            "patient_iid": patient.patient_iid,
            "age": patient.age,
            "gender": patient.gender,
            "clinical_notes": patient.clinical_notes,
            "additional_info": patient.additional_info,
            "created_at": patient.created_at.isoformat(),
            "updated_at": patient.updated_at.isoformat(),
        }
        sync_patient_to_fastapi(patient_dict)

        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response_data.pop('password', None)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class PatientProfileCompletionView(generics.UpdateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        required_fields = ['age', 'gender']
        missing_fields = [field for field in required_fields if field not in request.data]

        if missing_fields:
            return Response(
                {'error': f'Campos obrigatórios para sessão: {", ".join(missing_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = super().update(request, *args, **kwargs, partial=True)

        patient = self.get_object()
        patient_dict = {
            "patient_iid": patient.patient_iid,
            "age": patient.age,
            "gender": patient.gender,
            "clinical_notes": patient.clinical_notes,
            "additional_info": patient.additional_info,
            "created_at": patient.created_at.isoformat(),
            "updated_at": patient.updated_at.isoformat(),
        }
        sync_patient_to_fastapi(patient_dict)

        return response


class PatientListView(ScientistIDMixin, generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        scientist = self.get_scientist()
        is_test = self.request.query_params.get('is_test', None)
        queryset = Patient.objects.filter(scientist=scientist)

        if is_test is not None:
            queryset = queryset.filter(is_test=is_test.lower() == 'true')
        return queryset


class PatientDetailView(ScientistIDMixin, generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        scientist = self.get_scientist()
        return Patient.objects.filter(scientist=scientist)


class ScientistUpdatePatientView(ScientistIDMixin, generics.UpdateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        scientist = self.get_scientist()
        return Patient.objects.filter(scientist=scientist)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs, partial=True)

        patient = self.get_object()
        patient_dict = {
            "patient_iid": patient.patient_iid,
            "age": patient.age,
            "gender": patient.gender,
            "clinical_notes": patient.clinical_notes,
            "additional_info": patient.additional_info,
            "created_at": patient.created_at.isoformat(),
            "updated_at": patient.updated_at.isoformat(),
        }
        sync_patient_to_fastapi(patient_dict)

        return response


class AvailablePatientsListView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Patient.objects.filter(scientist__isnull=True, is_test=False)


class LinkPatientToScientistView(ScientistIDMixin, generics.UpdateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']
    
    def get_queryset(self):
        return Patient.objects.filter(scientist__isnull=True, is_test=False)
    
    def patch(self, request, *args, **kwargs):
        patient = self.get_object()
        scientist = self.get_scientist()

        patient.scientist = scientist
        patient.save()
        
        serializer = self.get_serializer(patient)

        patient_dict = {
            "patient_iid": patient.patient_iid,
            "age": patient.age,
            "gender": patient.gender,
            "clinical_notes": patient.clinical_notes,
            "additional_info": patient.additional_info,
            "created_at": patient.created_at.isoformat(),
            "updated_at": patient.updated_at.isoformat(),
        }
        sync_patient_to_fastapi(patient_dict)

        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_session_eligibility(request):
    if not hasattr(request.user, 'id'):  # ou checar se request.user é Patient
        return Response(
            {'error': 'Esta funcionalidade é apenas para pacientes'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    patient = request.user
    required_fields = {
        'age': patient.age is not None,
        'gender': patient.gender is not None and patient.gender.strip() != ''
    }

    is_eligible = all(required_fields.values())

    return Response({
        'eligible': is_eligible,
        'missing_fields': [field for field, present in required_fields.items() if not present],
        'patient_data': PatientSerializer(patient).data
    })