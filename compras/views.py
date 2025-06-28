from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Proveedor, OrdenCompra, DetalleOrdenCompra
from .serializers import ProveedorSerializer, OrdenCompraSerializer, DetalleOrdenCompraSerializer
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=['Proveedores'],
    description="Login de usuario (obtener JWT token)"
)
class ProveedorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

@extend_schema(
    tags=['Ordenes de compra'],
    description="Login de usuario (obtener JWT token)"
)
class OrdenCompraViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = OrdenCompra.objects.all()
    serializer_class = OrdenCompraSerializer

@extend_schema(
    tags=['Detalles de compra'],
    description="Login de usuario (obtener JWT token)"
)
class DetalleOrdenCompraViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = DetalleOrdenCompra.objects.all()
    serializer_class = DetalleOrdenCompraSerializer
