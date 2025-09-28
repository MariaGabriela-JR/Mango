from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.models import BlacklistedToken
from patients.models import Patient
from scientists.models import Scientist
from patients.serializers import PatientSerializer
from scientists.serializers import ScientistSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import PatientLoginSerializer, ScientistLoginSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model

class PatientLoginViewJWT(TokenObtainPairView):
    serializer_class = PatientLoginSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

class ScientistLoginView(TokenObtainPairView):
    serializer_class = ScientistLoginSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get(self, request):
        user = request.user

        if isinstance(user, Patient):
            serializer = PatientSerializer(user)
            return Response({
                "user_type": "patient",
                "data": serializer.data
            })
        
        elif isinstance(user, Scientist):
            serializer = ScientistSerializer(user)
            return Response({
                "user_type": "scientist",
                "data": serializer.data
            })

        return Response({"detail": "User type invalid"}, status=400)
    
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token was not given"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
        except TokenError:
            return Response(
                {"detail": "Invalid token or already expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Salva o token na blacklist
        BlacklistedToken.objects.get_or_create(token=str(token))

        return Response({"detail": "Logout made with success"}, status=status.HTTP_200_OK)
    
class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user