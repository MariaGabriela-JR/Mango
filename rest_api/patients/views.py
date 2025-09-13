from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.generics import get_object_or_404

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

        for field in ['age', 'gender', 'clinical_notes', 'additional_info', 'groups', 'user_permissions', 'scientist', 'is_test']:
            data.pop(field, None)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

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

        for field in ['age', 'gender', 'clinical_notes', 'additional_info', 'groups', 'user_permissions', 'scientist', 'is_test']:
            data.pop(field, None)

        data['is_test'] = False

        if request.user.is_authenticated and hasattr(request.user, 'scientist_id'):
            data['scientist'] = request.user.id
        else:
            data['scientist'] = None

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

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
        return super().update(request, *args, **kwargs, partial=True)
    
class PatientListView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            is_test = self.request.query_params.get('is_test', None)
            queryset = Patient.objects.filter(scientist=self.request.user)

            if is_test is not None:
                queryset = queryset.filter(is_test=is_test.lower() == 'true')

            return queryset
        return Patient.objects.none()

class PatientDetailView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            return Patient.objects.filter(scientist=self.request.user)
        return Patient.objects.none()
    
class ScientistUpdatePatientView(generics.UpdateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            return Patient.objects.filter(scientist=self.request.user)
        return Patient.objects.none()
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj
    
    def update(self, request, *args, **kwargs):
        patient = self.get_object()
        
        serializer = self.get_serializer(patient, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
class AvailablePatientsListView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            return Patient.objects.filter(scientist__isnull=True, is_test=False)
        return Patient.objects.none()
    
class LinkPatientToScientistView(generics.UpdateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']
    
    def get_queryset(self):
        return Patient.objects.filter(scientist__isnull=True, is_test=False)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj
    
    def patch(self, request, *args, **kwargs):
        patient = self.get_object()
        
        patient.scientist = request.user
        patient.save()
        
        serializer = self.get_serializer(patient)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])

def check_session_eligibility(request):
    if not hasattr(request.user, 'patient_iid'):
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