from rest_framework import serializers
from .models import Proveedor, OrdenCompra, DetalleOrdenCompra
from inventario.models import Producto  # Relación con producto
from inventario.serializers import ProductoSerializer  # Para mostrar info anidada si se desea


# Proveedor
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


# Detalle de Orden de Compra
class DetalleOrdenCompraSerializer(serializers.ModelSerializer):
    producto_detalle = ProductoSerializer(source='producto', read_only=True)
    
    class Meta:
        model = DetalleOrdenCompra
        fields = [
            'id',
            'orden_compra',
            'producto',
            'producto_detalle',
            'cantidad',
            'precio_unitario',
            'subtotal'
        ]
        extra_kwargs = {
            'subtotal': {'read_only': True}  # Esto hace que no sea requerido en el input
        }


# Orden de Compra con detalles anidados
class OrdenCompraSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenCompraSerializer(many=True, read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    creado_por_username = serializers.CharField(source='creado_por.username', read_only=True)

    class Meta:
        model = OrdenCompra
        fields = [
            'id',
            'numero',
            'proveedor',
            'proveedor_nombre',
            'estado',
            'fecha_orden',
            'fecha_entrega_estimada',
            'total',
            'observaciones',
            'creado_por',
            'creado_por_username',
            'detalles'
        ]
