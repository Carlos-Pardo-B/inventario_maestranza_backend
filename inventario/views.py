from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import (
    Producto, Categoria, Ubicacion, Etiqueta, ProductoEtiqueta,
    Lote, MovimientoInventario, Kit, ComponenteKit
)
from .serializers import (
    ProductoSerializer, CategoriaSerializer, UbicacionSerializer, EtiquetaSerializer,
    ProductoEtiquetaSerializer, LoteSerializer, MovimientoInventarioSerializer,
    KitSerializer, ComponenteKitSerializer
)

from drf_spectacular.utils import extend_schema
# Create your views here.


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
    queryset = MovimientoInventario.objects.all()
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
