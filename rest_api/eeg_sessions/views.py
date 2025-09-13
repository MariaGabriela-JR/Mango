from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import EEGSession
from .serializers import EEGSessionSerializer, EEGSessionCreateSerializer, EEGSessionUpdateSerializer

class EEGSessionCreateView(generics.CreateAPIView):
    queryset = EEGSession.objects.all()
    serializer_class = EEGSessionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(scientist=self.request.user)

class EEGSessionListView(generics.ListAPIView):
    serializer_class = EEGSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            return EEGSession.objects.filter(scientist=self.request.user)
        return EEGSession.objects.none()

class EEGSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EEGSessionUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            return EEGSession.objects.filter(scientist=self.request.user)
        return EEGSession.objects.none()

class EEGSessionSyncFastAPIView(generics.UpdateAPIView):
    serializer_class = EEGSessionUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            return EEGSession.objects.filter(scientist=self.request.user)
        return EEGSession.objects.none()

    def patch(self, request, *args, **kwargs):
        session = self.get_object()
        
        sync_fields = [
            'edf_file_id', 'trial_index', 'start_time', 'duration',
            'emotion_category', 'description', 'parameters', 'status'
        ]
        
        data = {k: v for k, v in request.data.items() if k in sync_fields}
        
        serializer = self.get_serializer(session, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

class EEGSessionUpdateDataView(generics.UpdateAPIView):
    serializer_class = EEGSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            return EEGSession.objects.filter(scientist=self.request.user)
        return EEGSession.objects.none()

class EEGSessionChangeStatusView(generics.UpdateAPIView):
    serializer_class = EEGSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            return EEGSession.objects.filter(scientist=self.request.user)
        return EEGSession.objects.none()

class EEGSessionByPatientView(generics.ListAPIView):
    serializer_class = EEGSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            patient_id = self.kwargs['patient_id']
            return EEGSession.objects.filter(scientist=self.request.user, patient_id=patient_id)
        return EEGSession.objects.none()

class EEGSessionByStatusView(generics.ListAPIView):
    serializer_class = EEGSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'scientist_id'):
            status = self.kwargs['status']
            return EEGSession.objects.filter(scientist=self.request.user, status=status)
        return EEGSession.objects.none()