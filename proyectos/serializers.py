from rest_framework import serializers
from .models import Proyecto
from usuarios.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name', 'rol']

class ProyectoSerializer(serializers.ModelSerializer):
    responsable_detail = UsuarioSerializer(source='responsable', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Proyecto
        fields = [
            'id', 'codigo', 'nombre', 'descripcion', 'estado', 'estado_display',
            'fecha_inicio', 'fecha_fin_estimada', 'fecha_fin_real',
            'responsable', 'responsable_detail'
        ]
        extra_kwargs = {
            'responsable': {'write_only': True}
        }

class ProyectoEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ['id', 'estado']