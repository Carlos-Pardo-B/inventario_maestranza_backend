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

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer

class ProductoEtiquetaViewSet(viewsets.ModelViewSet):
    queryset = ProductoEtiqueta.objects.all()
    serializer_class = ProductoEtiquetaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer

class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer

class ComponenteKitViewSet(viewsets.ModelViewSet):
    queryset = ComponenteKit.objects.all()
    serializer_class = ComponenteKitSerializer
