from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Proyecto
from .serializers import ProyectoSerializer, ProyectoEstadoSerializer
from usuarios.models import Usuario
from django.shortcuts import get_object_or_404

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros opcionales
        estado = self.request.query_params.get('estado', None)
        responsable = self.request.query_params.get('responsable', None)
        
        if estado:
            queryset = queryset.filter(estado=estado)
        if responsable:
            queryset = queryset.filter(responsable=responsable)
            
        return queryset.order_by('-fecha_inicio')

    @action(detail=True, methods=['patch'], serializer_class=ProyectoEstadoSerializer)
    def cambiar_estado(self, request, pk=None):
        proyecto = self.get_object()
        serializer = self.get_serializer(proyecto, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # Si el estado es COMPLETADO o CANCELADO, establecer fecha_fin_real
            estado = serializer.validated_data.get('estado')
            if estado in ['COMPLETADO', 'CANCELADO']:
                proyecto.fecha_fin_real = timezone.now().date()
                proyecto.save()
            
            return Response(ProyectoSerializer(proyecto).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def estados_disponibles(self, request):
        return Response([{'value': e[0], 'display': e[1]} for e in Proyecto.ESTADOS])

    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)