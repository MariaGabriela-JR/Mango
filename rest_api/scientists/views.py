from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Scientist
from .serializers import ScientistSerializer
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail

class ScientistCreateView(generics.CreateAPIView):
    queryset = Scientist.objects.all()
    serializer_class = ScientistSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        for field in ['groups', 'user_permissions', 'is_verified']:
            data.pop(field, None)

        required_fields = ['institution', 'specialization']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response(
                {'error': f'Campos obrigatórios: {", ".join(missing_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data['is_verified'] = False
        verification_token = get_random_string(50)
        data['verification_token'] = verification_token
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        scientist = serializer.save()

        self.send_approval_email(scientist, verification_token)

        response_data = serializer.data
        response_data.pop('password', None)
        response_data['message'] = 'Conta criada. Aguarde verificação administrativa.'

        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def send_approval_email(self, scientist, token):
        subject = 'Nova conta de cientista precisa de verificação'
        message = f'''
        Nova conta de cientista criada:

        Nome: {scientist.first_name} {scientist.last_name}
        Email: {scientist.email}
        Instituição: {scientist.institution}
        Especialização: {scientist.specialization}

        Link para aprovar: {settings.FRONTEND_URL}/admin/verify-scientist/{token}/
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
    
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

    send_mail(
        'Sua conta foi aprovada!',
        'Sua conta de cientista foi verificada e aprovada!',
        settings.DEFAULT_FROM_EMAIL,
        [scientist.email],
        fail_silently=False,
    )

    return Response({'status': 'Cientista verificado com sucesso.'})