from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions,  generics
from .serializers import (
    UsuarioSerializer,
    UsuarioListSerializer,
    RegistroUsuarioSerializer,
    LoginSerializer
)
from .models import Usuario
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema
# Create your views here.
@extend_schema(
    tags=['Autenticación'],
    description="Login de usuario (obtener JWT token)"
)
class LoginView(APIView):
    permission_classes = []  # Login no requiere token previo

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)

from .serializers import RegistroUsuarioSerializer


@extend_schema(
    tags=['Usuarios'],
    description="Registro de usuarios"
)
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
    
@extend_schema(
    tags=['Usuarios'],
    description="Lista todos los usuarios con capacidad de filtrado"
)
class UsuarioListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['rol', 'activo']  # Campos permitidos para filtrar
    search_fields = ['username', 'email']  # Campos para búsqueda

@extend_schema(
    tags=['Usuarios'],
    description="Detalle de un usuario específico"
)
class UsuarioDetailView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Usuarios solo pueden ver su propio perfil, admin puede ver cualquiera
        if self.request.user.is_superuser:
            return super().get_object()
        return self.request.user

@extend_schema(
    tags=['Usuarios'],
    description="Actualiza un usuario existente"
)
class UsuarioUpdateView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Usuarios solo pueden editar su propio perfil, admin puede editar cualquiera
        if self.request.user.is_superuser:
            return super().get_object()
        return self.request.user

    def perform_update(self, serializer):
        # Evitamos que usuarios no admin cambien su rol
        if not self.request.user.is_superuser:
            serializer.validated_data.pop('rol', None)
            serializer.validated_data.pop('is_superuser', None)
        serializer.save()

@extend_schema(
    tags=['Usuarios'],
    description="Elimina un usuario (solo admin)"
)
class UsuarioDeleteView(generics.DestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # No permitimos eliminar el propio usuario admin
        if instance == request.user:
            return Response(
                {"detail": "No puedes eliminarte a ti mismo."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)