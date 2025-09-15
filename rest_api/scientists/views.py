from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .models import Scientist
from .serializers import ScientistSerializer
from django.utils.crypto import get_random_string
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Scientist
from .serializers import ScientistSerializer
from datetime import timedelta


class ScientistCreateView(generics.CreateAPIView):
    queryset = Scientist.objects.all()
    serializer_class = ScientistSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Remove campos que não devem ser passados no serializer
        for field in ['groups', 'user_permissions', 'is_verified']:
            data.pop(field, None)

        # Verifica campos obrigatórios
        required_fields = ['institution', 'specialization']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return Response(
                {'error': f'Campos obrigatórios: {", ".join(missing_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Gera token de verificação
        verification_token = get_random_string(50)

        # Serializa e salva o cientista
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        scientist = serializer.save(
            is_verified=False,
            verification_token=verification_token
        )

        # Gera token de registro temporário (para acesso à página de sucesso)
        refresh = RefreshToken.for_user(scientist)
        refresh.access_token.set_exp(lifetime=timedelta(minutes=2))
        registration_access_token = str(refresh.access_token)

        # Prepara a resposta
        response_data = serializer.data
        response_data.pop('password', None)
        response_data['message'] = 'Conta criada com sucesso.'
        response_data['verification_token'] = verification_token
        response_data['registration_token'] = registration_access_token

        return Response(response_data, status=status.HTTP_201_CREATED)

class ScientistProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ScientistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def verify_scientists(request, token):
    scientist = get_object_or_404(Scientist, verification_token=token)

    scientist.is_verified = True
    scientist.verification_token = None
    scientist.save()

    return Response({'status': 'Cientista verificado com sucesso.'})