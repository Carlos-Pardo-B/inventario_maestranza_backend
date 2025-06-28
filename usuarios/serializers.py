from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 
            'email', 'rol', 'rol_display', 'telefono', 
            'activo', 'fecha_creacion'  # Elimina fecha_modificacion de aquí
        ]
        read_only_fields = [
            'id', 'fecha_creacion', 
            'rol_display'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UsuarioListSerializer(serializers.ModelSerializer):
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'rol_display', 'activo']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Credenciales incorrectas.")
        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo.")
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': {
                'id': user.id,
                'username': user.username,
                'rol': user.rol,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        }

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label='Confirmar password')

    class Meta:
        model = Usuario
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 'rol', 'telefono']
        extra_kwargs = {
            'rol': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Eliminamos el campo de confirmación
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            rol=validated_data['rol'],
            telefono=validated_data.get('telefono', '')
        )
        return user