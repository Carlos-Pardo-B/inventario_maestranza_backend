from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, RegistroUsuarioSerializer, UsuarioSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class LoginView(APIView):
    permission_classes = []  # Login no requiere token previo

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)

from .serializers import RegistroUsuarioSerializer
from rest_framework.permissions import AllowAny

class RegistroView(APIView):
    permission_classes = [AllowAny]  # Permite registro sin autenticación

    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Opcional: enviar token inmediatamente después del registro
            refresh = RefreshToken.for_user(user)
            return Response({
                'usuario': UsuarioSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)