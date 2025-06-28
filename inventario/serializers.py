from rest_framework import serializers
from .models import (
    Producto, Categoria, Ubicacion, Etiqueta, ProductoEtiqueta,
    Lote, Movimiento, Kit, ComponenteKit, AlertaStock
)

# Categoría
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

# Ubicación
class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'

# Etiqueta
class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'

# ProductoEtiqueta (intermedia)
class ProductoEtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoEtiqueta
        fields = '__all__'

# Producto
class ProductoSerializer(serializers.ModelSerializer):
    stock_actual = serializers.ReadOnlyField()
    requiere_reposicion = serializers.ReadOnlyField()

    class Meta:
        model = Producto
        fields = '__all__'

# Lote
class LoteSerializer(serializers.ModelSerializer):
    cantidad_actual = serializers.ReadOnlyField()
    esta_vencido = serializers.ReadOnlyField()

    class Meta:
        model = Lote
        fields = '__all__'

# Movimiento
class MovimientoInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'

# ComponenteKit
class ComponenteKitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponenteKit
        fields = '__all__'

# Kit
class KitSerializer(serializers.ModelSerializer):
    componentes = ComponenteKitSerializer(many=True, read_only=True)
    disponible = serializers.ReadOnlyField()

    class Meta:
        model = Kit
        fields = '__all__'

class AlertaStockSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_codigo = serializers.CharField(source='producto.codigo', read_only=True)
    
    class Meta:
        model = AlertaStock
        fields = [
            'id', 'producto', 'producto_nombre', 'producto_codigo',
            'nivel_alerta', 'stock_actual', 'estado', 'fecha_creacion',
            'comentarios'
        ]
        read_only_fields = ('fecha_creacion', 'stock_actual', 'creada_por')

class ProductoAlertasSerializer(serializers.ModelSerializer):
    alertas_pendientes = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id', 'codigo', 'nombre', 'stock_actual',
            'stock_minimo', 'stock_regular', 'stock_maximo',
            'alertas_pendientes'
        ]