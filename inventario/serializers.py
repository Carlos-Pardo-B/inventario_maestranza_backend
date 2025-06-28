from rest_framework import serializers
from .models import (
    Producto, Categoria, Ubicacion, Etiqueta, ProductoEtiqueta,
    Lote, MovimientoInventario, Kit, ComponenteKit
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
        model = MovimientoInventario
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
