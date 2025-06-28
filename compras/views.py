from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Proveedor, OrdenCompra, DetalleOrdenCompra
from .serializers import ProveedorSerializer, OrdenCompraSerializer, DetalleOrdenCompraSerializer
from rest_framework.permissions import AllowAny

class ProveedorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


class OrdenCompraViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = OrdenCompra.objects.all()
    serializer_class = OrdenCompraSerializer


class DetalleOrdenCompraViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = DetalleOrdenCompra.objects.all()
    serializer_class = DetalleOrdenCompraSerializer
