from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PatientLoginSerializer, ScientistLoginSerializer

class PatientLoginViewJWT(TokenObtainPairView):
    serializer_class = PatientLoginSerializer
    parser_classes = [FormParser, MultiPartParser]

class ScientistLoginView(TokenObtainPairView):
    serializer_class = ScientistLoginSerializer
    parser_classes = [FormParser, MultiPartParser]
