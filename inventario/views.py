from django.shortcuts import render
from django.db import models  
# Create your views here.
from rest_framework import viewsets
from .models import (
    Producto, Categoria, Ubicacion, Etiqueta, ProductoEtiqueta,
    Lote, Movimiento, Kit, ComponenteKit, AlertaStock
)
from .serializers import (
    ProductoSerializer, CategoriaSerializer, UbicacionSerializer, EtiquetaSerializer,
    ProductoEtiquetaSerializer, LoteSerializer, MovimientoInventarioSerializer,
    KitSerializer, ComponenteKitSerializer
)

from drf_spectacular.utils import extend_schema
# Create your views here.
from .serializers import AlertaStockSerializer, ProductoAlertasSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

User = get_user_model()

@extend_schema(
    tags=['Categoria'],
    description="Login de usuario (obtener JWT token)"
)
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


@extend_schema(
    tags=['Ubicaciónes'],
    description="Login de usuario (obtener JWT token)"
)
class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer
    
@extend_schema(
    tags=['Etiquetas'],
    description="Login de usuario (obtener JWT token)"
)
class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer

@extend_schema(
    tags=['Producto Etiqueta'],
    description="Login de usuario (obtener JWT token)"
)
class ProductoEtiquetaViewSet(viewsets.ModelViewSet):
    queryset = ProductoEtiqueta.objects.all()
    serializer_class = ProductoEtiquetaSerializer

@extend_schema(
    tags=['Productos'],
    description="Login de usuario (obtener JWT token)"
)
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    

@extend_schema(
    tags=['Lotes'],
    description="Login de usuario (obtener JWT token)"
)
class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

@extend_schema(
    tags=['Movimiento Inventario'],
    description="Login de usuario (obtener JWT token)"
)
class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoInventarioSerializer

@extend_schema(
    tags=['Kits'],
    description="Login de usuario (obtener JWT token)"
)
class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer

@extend_schema(
    tags=['Kit de Componentes'],
    description="Login de usuario (obtener JWT token)"
)
class ComponenteKitViewSet(viewsets.ModelViewSet):
    queryset = ComponenteKit.objects.all()
    serializer_class = ComponenteKitSerializer

class AlertaStockViewSet(viewsets.ModelViewSet):
    queryset = AlertaStock.objects.select_related('producto', 'creada_por', 'resuelta_por')
    serializer_class = AlertaStockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nivel_alerta', 'estado', 'producto']
    search_fields = ['producto__nombre', 'producto__codigo']
    ordering_fields = ['fecha_creacion', 'nivel_alerta']
    ordering = ['-fecha_creacion']

    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        alerta = self.get_object()
        alerta.estado = 'RESUELTA'
        alerta.resuelta_por = request.user
        alerta.save()
        return Response({'status': 'Alerta resuelta'})

    @action(detail=True, methods=['post'])
    def descartar(self, request, pk=None):
        alerta = self.get_object()
        alerta.estado = 'DESCARTADA'
        alerta.resuelta_por = request.user
        alerta.save()
        return Response({'status': 'Alerta descartada'})

@extend_schema(
    tags=['Productos con Alertas'],
    description="Productos con alertas de stock"
)
class ProductoAlertasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.annotate(
        alertas_pendientes=models.Count(
            models.Case(
                models.When(alertas__estado='PENDIENTE', then=1),
                output_field=models.IntegerField()
            )
        )
    )
    serializer_class = ProductoAlertasSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria', 'activo']
    search_fields = ['nombre', 'codigo']

    @extend_schema(
        description="Lista de productos con stock crítico",
        parameters=[
            OpenApiParameter(name='categoria', description='Filtrar por categoría ID', required=False, type=int),
            OpenApiParameter(name='search', description='Búsqueda por nombre o código', required=False, type=str),
        ]
    )
    @action(detail=False, methods=['get'])
    def criticos(self, request):
        productos = Producto.objects.filter(
            stock_actual__lte=models.F('stock_minimo')
        ).order_by('stock_actual')
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)
    
class AlertaStockBajoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AlertaStock.objects.filter(
        nivel_alerta='MINIMO',
        estado='PENDIENTE'
    ).select_related('producto', 'creada_por', 'resuelta_por')
    
    serializer_class = AlertaStockSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['producto__nombre', 'producto__codigo']
    ordering_fields = ['fecha_creacion']
    ordering = ['-fecha_creacion']

    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        alerta = self.get_object()
        alerta.estado = 'RESUELTA'
        alerta.resuelta_por = request.user
        alerta.save()
        return Response({'status': 'Alerta de stock bajo resuelta'})