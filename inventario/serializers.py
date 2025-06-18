# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Proveedor, Categoria, Ubicacion, Producto, Etiqueta, ProductoEtiqueta,
    Lote, Kit, ComponenteKit, Proyecto, MovimientoInventario, OrdenCompra,
    DetalleOrdenCompra, Alerta, AuditoriaInventario, DetalleAuditoria
)

User = get_user_model()

# Serializers para Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'rol', 'telefono', 'activo', 'password', 'fecha_creacion']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UsuarioListSerializer(serializers.ModelSerializer):
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'rol', 'rol_display', 'telefono', 'activo', 'fecha_creacion']


# Serializers para Proveedor
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProveedorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'codigo', 'nombre', 'rut', 'telefono', 'email', 'activo']


# Serializers para Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    productos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'codigo', 'activo', 'productos_count']
    
    def get_productos_count(self, obj):
        return obj.producto_set.count()


# Serializers para Ubicacion
class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'

class UbicacionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = ['id', 'codigo', 'nombre', 'seccion', 'activo']


# Serializers para Etiqueta
class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'


# Serializers para Producto
class ProductoListSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    stock_actual = serializers.ReadOnlyField()
    requiere_reposicion = serializers.ReadOnlyField()
    unidad_medida_display = serializers.CharField(source='get_unidad_medida_display', read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'nombre', 'categoria_nombre', 'unidad_medida', 
                 'unidad_medida_display', 'stock_actual', 'stock_minimo', 
                 'requiere_reposicion', 'activo', 'precio_promedio']

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    creado_por_nombre = serializers.CharField(source='creado_por.get_full_name', read_only=True)
    stock_actual = serializers.ReadOnlyField()
    requiere_reposicion = serializers.ReadOnlyField()
    etiquetas = EtiquetaSerializer(many=True, read_only=True, source='productoetiqueta_set.etiqueta')
    
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoCreateUpdateSerializer(serializers.ModelSerializer):
    etiquetas_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    
    class Meta:
        model = Producto
        exclude = ['creado_por']
    
    def create(self, validated_data):
        etiquetas_ids = validated_data.pop('etiquetas_ids', [])
        validated_data['creado_por'] = self.context['request'].user
        producto = super().create(validated_data)
        
        # Asignar etiquetas
        for etiqueta_id in etiquetas_ids:
            ProductoEtiqueta.objects.create(producto=producto, etiqueta_id=etiqueta_id)
        
        return producto
    
    def update(self, instance, validated_data):
        etiquetas_ids = validated_data.pop('etiquetas_ids', None)
        producto = super().update(instance, validated_data)
        
        if etiquetas_ids is not None:
            # Eliminar etiquetas existentes y crear nuevas
            ProductoEtiqueta.objects.filter(producto=producto).delete()
            for etiqueta_id in etiquetas_ids:
                ProductoEtiqueta.objects.create(producto=producto, etiqueta_id=etiqueta_id)
        
        return producto


# Serializers para Lote
class LoteSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    cantidad_actual = serializers.ReadOnlyField()
    esta_vencido = serializers.ReadOnlyField()
    dias_para_vencer = serializers.SerializerMethodField()
    
    class Meta:
        model = Lote
        fields = '__all__'
    
    def get_dias_para_vencer(self, obj):
        if obj.fecha_vencimiento:
            from django.utils import timezone
            dias = (obj.fecha_vencimiento - timezone.now().date()).days
            return dias if dias >= 0 else 0
        return None

class LoteListSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    cantidad_actual = serializers.ReadOnlyField()
    esta_vencido = serializers.ReadOnlyField()
    
    class Meta:
        model = Lote
        fields = ['id', 'codigo', 'producto_nombre', 'fecha_vencimiento', 
                 'cantidad_actual', 'esta_vencido', 'fecha_ingreso']


# Serializers para Kit
class ComponenteKitSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_stock = serializers.CharField(source='producto.stock_actual', read_only=True)
    
    class Meta:
        model = ComponenteKit
        fields = ['id', 'producto', 'producto_nombre', 'producto_stock', 'cantidad']

class KitSerializer(serializers.ModelSerializer):
    componentes = ComponenteKitSerializer(many=True, read_only=True)
    disponible = serializers.ReadOnlyField()
    
    class Meta:
        model = Kit
        fields = '__all__'

class KitCreateUpdateSerializer(serializers.ModelSerializer):
    componentes = ComponenteKitSerializer(many=True, write_only=True)
    
    class Meta:
        model = Kit
        exclude = ['fecha_creacion']
    
    def create(self, validated_data):
        componentes_data = validated_data.pop('componentes')
        kit = Kit.objects.create(**validated_data)
        
        for componente_data in componentes_data:
            ComponenteKit.objects.create(kit=kit, **componente_data)
        
        return kit
    
    def update(self, instance, validated_data):
        componentes_data = validated_data.pop('componentes', None)
        kit = super().update(instance, validated_data)
        
        if componentes_data is not None:
            # Eliminar componentes existentes y crear nuevos
            kit.componentes.all().delete()
            for componente_data in componentes_data:
                ComponenteKit.objects.create(kit=kit, **componente_data)
        
        return kit


# Serializers para Proyecto
class ProyectoSerializer(serializers.ModelSerializer):
    responsable_nombre = serializers.CharField(source='responsable.get_full_name', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Proyecto
        fields = '__all__'

class ProyectoListSerializer(serializers.ModelSerializer):
    responsable_nombre = serializers.CharField(source='responsable.get_full_name', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Proyecto
        fields = ['id', 'codigo', 'nombre', 'estado', 'estado_display', 
                 'fecha_inicio', 'fecha_fin_estimada', 'responsable_nombre']


# Serializers para MovimientoInventario
class MovimientoInventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    ubicacion_origen_nombre = serializers.CharField(source='ubicacion_origen.nombre', read_only=True)
    ubicacion_destino_nombre = serializers.CharField(source='ubicacion_destino.nombre', read_only=True)
    proyecto_nombre = serializers.CharField(source='proyecto.nombre', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    valor_total = serializers.SerializerMethodField()
    
    class Meta:
        model = MovimientoInventario
        fields = '__all__'
    
    def get_valor_total(self, obj):
        if obj.precio_unitario:
            return obj.cantidad * obj.precio_unitario
        return None

class MovimientoInventarioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoInventario
        exclude = ['usuario', 'numero']
    
    def create(self, validated_data):
        # Generar número automático
        from django.utils import timezone
        fecha = timezone.now()
        numero = f"MOV-{fecha.strftime('%Y%m%d')}-{MovimientoInventario.objects.count() + 1:04d}"
        
        validated_data['usuario'] = self.context['request'].user
        validated_data['numero'] = numero
        
        return super().create(validated_data)


# Serializers para OrdenCompra
class DetalleOrdenCompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = DetalleOrdenCompra
        fields = '__all__'

class OrdenCompraSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    creado_por_nombre = serializers.CharField(source='creado_por.get_full_name', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    detalles = DetalleOrdenCompraSerializer(many=True, read_only=True)
    
    class Meta:
        model = OrdenCompra
        fields = '__all__'

class OrdenCompraCreateSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenCompraSerializer(many=True, write_only=True)
    
    class Meta:
        model = OrdenCompra
        exclude = ['creado_por', 'numero', 'total']
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        
        # Generar número automático
        from django.utils import timezone
        fecha = timezone.now()
        numero = f"OC-{fecha.strftime('%Y%m%d')}-{OrdenCompra.objects.count() + 1:04d}"
        
        validated_data['creado_por'] = self.context['request'].user
        validated_data['numero'] = numero
        
        orden = OrdenCompra.objects.create(**validated_data)
        
        total = 0
        for detalle_data in detalles_data:
            detalle = DetalleOrdenCompra.objects.create(orden_compra=orden, **detalle_data)
            total += detalle.subtotal
        
        orden.total = total
        orden.save()
        
        return orden


# Serializers para Alerta
class AlertaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    nivel_display = serializers.CharField(source='get_nivel_display', read_only=True)
    usuario_asignado_nombre = serializers.CharField(source='usuario_asignado.get_full_name', read_only=True)
    
    class Meta:
        model = Alerta
        fields = '__all__'


# Serializers para Auditoria
class DetalleAuditoriaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    ubicacion_nombre = serializers.CharField(source='ubicacion.nombre', read_only=True)
    
    class Meta:
        model = DetalleAuditoria
        fields = '__all__'

class AuditoriaInventarioSerializer(serializers.ModelSerializer):
    auditor_nombre = serializers.CharField(source='auditor.get_full_name', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    detalles = DetalleAuditoriaSerializer(many=True, read_only=True)
    
    class Meta:
        model = AuditoriaInventario
        fields = '__all__'

class AuditoriaInventarioCreateSerializer(serializers.ModelSerializer):
    detalles = DetalleAuditoriaSerializer(many=True, write_only=True, required=False)
    
    class Meta:
        model = AuditoriaInventario
        exclude = ['codigo']
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        
        # Generar código automático
        from django.utils import timezone
        fecha = timezone.now()
        codigo = f"AUD-{fecha.strftime('%Y%m%d')}-{AuditoriaInventario.objects.count() + 1:03d}"
        
        validated_data['codigo'] = codigo
        auditoria = AuditoriaInventario.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            DetalleAuditoria.objects.create(auditoria=auditoria, **detalle_data)
        
        return auditoria


# Serializers para reportes y estadísticas
class StockBajoSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    codigo = serializers.CharField()
    nombre = serializers.CharField()
    stock_actual = serializers.IntegerField()
    stock_minimo = serializers.IntegerField()
    diferencia = serializers.IntegerField()

class ResumenInventarioSerializer(serializers.Serializer):
    total_productos = serializers.IntegerField()
    productos_activos = serializers.IntegerField()
    productos_stock_bajo = serializers.IntegerField()
    valor_total_inventario = serializers.DecimalField(max_digits=15, decimal_places=2)
    movimientos_mes = serializers.IntegerField()

class MovimientosPorTipoSerializer(serializers.Serializer):
    tipo = serializers.CharField()
    cantidad_movimientos = serializers.IntegerField()
    total_productos = serializers.IntegerField()