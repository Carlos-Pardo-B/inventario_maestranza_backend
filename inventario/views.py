from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .models import (
    Proveedor, Categoria, Ubicacion, Producto, Etiqueta, ProductoEtiqueta,
    Lote, Kit, ComponenteKit, Proyecto, MovimientoInventario, OrdenCompra,
    DetalleOrdenCompra, Alerta, AuditoriaInventario, DetalleAuditoria
)
from .serializers import (
    UsuarioSerializer, UsuarioListSerializer,
    ProveedorSerializer, ProveedorListSerializer,
    CategoriaSerializer, UbicacionSerializer, UbicacionListSerializer,
    EtiquetaSerializer, ProductoSerializer, ProductoListSerializer, ProductoCreateUpdateSerializer,
    LoteSerializer, LoteListSerializer,
    KitSerializer, KitCreateUpdateSerializer,
    ProyectoSerializer, ProyectoListSerializer,
    MovimientoInventarioSerializer, MovimientoInventarioCreateSerializer,
    OrdenCompraSerializer, OrdenCompraCreateSerializer,
    AlertaSerializer,
    AuditoriaInventarioSerializer, AuditoriaInventarioCreateSerializer,
)
# Create your views here.
User = get_user_model()

# Usuarios
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UsuarioListSerializer
        return UsuarioSerializer


# Proveedores
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProveedorListSerializer
        return ProveedorSerializer


# Categorías
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


# Ubicaciones
class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return UbicacionListSerializer
        return UbicacionSerializer


# Etiquetas
class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer


# Productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()

    def get_serializer_class(self):
        if self.action in ['list']:
            return ProductoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductoCreateUpdateSerializer
        return ProductoSerializer


# Lotes
class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return LoteListSerializer
        return LoteSerializer


# Kits
class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KitCreateUpdateSerializer
        return KitSerializer


# Proyectos
class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProyectoListSerializer
        return ProyectoSerializer


# Movimientos de Inventario
class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return MovimientoInventarioCreateSerializer
        return MovimientoInventarioSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


# Órdenes de Compra
class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrdenCompraCreateSerializer
        return OrdenCompraSerializer

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)


# Alertas
class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer


# Auditorías
class AuditoriaInventarioViewSet(viewsets.ModelViewSet):
    queryset = AuditoriaInventario.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return AuditoriaInventarioCreateSerializer
        return AuditoriaInventarioSerializer
