from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from patients.models import Patient
from scientists.models import Scientist
from patients.serializers import PatientSerializer
from scientists.serializers import ScientistSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PatientLoginSerializer, ScientistLoginSerializer

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

        return Response({"detail": "Tipo de usuário invalido"}, status=400)