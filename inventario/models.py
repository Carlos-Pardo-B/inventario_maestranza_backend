from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

# Modelo de Usuario personalizado para los diferentes perfiles
class Usuario(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrador del Sistema'),
        ('GESTOR_INV', 'Gestor de Inventario'),
        ('COMPRADOR', 'Comprador'),
        ('LOGISTICA', 'Encargado de Logística'),
        ('JEFE_PROD', 'Jefe de Producción'),
        ('AUDITOR', 'Auditor de Inventario'),
        ('GERENTE_PROY', 'Gerente de Proyectos'),
        ('USUARIO_FINAL', 'Usuario Final/Trabajador de Planta'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='USUARIO_FINAL')
    telefono = models.CharField(max_length=15, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"

# Modelo para Proveedores
class Proveedor(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    contacto_principal = models.CharField(max_length=100)
    terminos_pago = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


# Modelo para Categorías de productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    codigo = models.CharField(max_length=20, unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


# Modelo para Ubicaciones físicas en el almacén
class Ubicacion(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    seccion = models.CharField(max_length=50)
    pasillo = models.CharField(max_length=10, blank=True)
    estante = models.CharField(max_length=10, blank=True)
    nivel = models.CharField(max_length=10, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"


# Modelo principal para Productos/Piezas
class Producto(models.Model):
    UNIDADES_MEDIDA = [
        ('UN', 'Unidad'),
        ('KG', 'Kilogramo'),
        ('LT', 'Litro'),
        ('MT', 'Metro'),
        ('M2', 'Metro Cuadrado'),
        ('M3', 'Metro Cúbico'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    numero_serie = models.CharField(max_length=100, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    unidad_medida = models.CharField(max_length=5, choices=UNIDADES_MEDIDA)
    precio_promedio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    stock_maximo = models.PositiveIntegerField(default=0)
    requiere_lote = models.BooleanField(default=False)
    tiene_vencimiento = models.BooleanField(default=False)
    dias_vencimiento = models.PositiveIntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def stock_actual(self):
        """Calcula el stock actual basado en los movimientos"""
        ingresos = self.movimientos.filter(tipo='INGRESO').aggregate(
            total=models.Sum('cantidad'))['total'] or 0
        salidas = self.movimientos.filter(tipo='SALIDA').aggregate(
            total=models.Sum('cantidad'))['total'] or 0
        return ingresos - salidas

    @property
    def requiere_reposicion(self):
        """Verifica si el stock actual está por debajo del mínimo"""
        return self.stock_actual <= self.stock_minimo

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


# Modelo para Etiquetas personalizadas
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#007bff')  # Color hexadecimal
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"


# Tabla intermedia para productos y etiquetas
class ProductoEtiqueta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'etiqueta')


# # Modelo para Lotes
# class Lote(models.Model):
#     codigo = models.CharField(max_length=50, unique=True)
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes')
#     fecha_ingreso = models.DateTimeField(auto_now_add=True)
#     fecha_vencimiento = models.DateField(null=True, blank=True)
#     proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
#     precio_compra = models.DecimalField(max_digits=12, decimal_places=2)
#     cantidad_inicial = models.PositiveIntegerField()
#     observaciones = models.TextField(blank=True)

#     def __str__(self):
#         return f"Lote {self.codigo} - {self.producto.nombre}"

#     @property
#     def cantidad_actual(self):
#         """Calcula la cantidad actual del lote"""
#         ingresos = self.movimientos.filter(tipo='INGRESO').aggregate(
#             total=models.Sum('cantidad'))['total'] or 0
#         salidas = self.movimientos.filter(tipo='SALIDA').aggregate(
#             total=models.Sum('cantidad'))['total'] or 0
#         return ingresos - salidas

#     @property
#     def esta_vencido(self):
#         """Verifica si el lote está vencido"""
#         if self.fecha_vencimiento:
#             from django.utils import timezone
#             return timezone.now().date() > self.fecha_vencimiento
#         return False

#     class Meta:
#         verbose_name = "Lote"
#         verbose_name_plural = "Lotes"


# # Modelo para Kits o Conjuntos
# class Kit(models.Model):
#     codigo = models.CharField(max_length=50, unique=True)
#     nombre = models.CharField(max_length=200)
#     descripcion = models.TextField()
#     activo = models.BooleanField(default=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.codigo} - {self.nombre}"

#     @property
#     def disponible(self):
#         """Verifica si el kit está disponible basado en sus componentes"""
#         for componente in self.componentes.all():
#             if componente.producto.stock_actual < componente.cantidad:
#                 return False
#         return True

#     class Meta:
#         verbose_name = "Kit"
#         verbose_name_plural = "Kits"


# # Modelo para componentes de Kits
# class ComponenteKit(models.Model):
#     kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name='componentes')
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
#     cantidad = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.kit.nombre} - {self.producto.nombre} (x{self.cantidad})"

#     class Meta:
#         unique_together = ('kit', 'producto')


# # Modelo para Proyectos
# class Proyecto(models.Model):
#     ESTADOS = [
#         ('PLANIFICADO', 'Planificado'),
#         ('EN_CURSO', 'En Curso'),
#         ('PAUSADO', 'Pausado'),
#         ('COMPLETADO', 'Completado'),
#         ('CANCELADO', 'Cancelado'),
#     ]

#     codigo = models.CharField(max_length=50, unique=True)
#     nombre = models.CharField(max_length=200)
#     descripcion = models.TextField()
#     estado = models.CharField(max_length=20, choices=ESTADOS, default='PLANIFICADO')
#     fecha_inicio = models.DateField()
#     fecha_fin_estimada = models.DateField()
#     fecha_fin_real = models.DateField(null=True, blank=True)
#     responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT)

#     def __str__(self):
#         return f"{self.codigo} - {self.nombre}"

#     class Meta:
#         verbose_name = "Proyecto"
#         verbose_name_plural = "Proyectos"


# # Modelo para Movimientos de Inventario
# class MovimientoInventario(models.Model):
#     TIPOS_MOVIMIENTO = [
#         ('INGRESO', 'Ingreso'),
#         ('SALIDA', 'Salida'),
#         ('TRANSFERENCIA', 'Transferencia'),
#         ('AJUSTE', 'Ajuste'),
#         ('DEVOLUCION', 'Devolución'),
#     ]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     numero = models.CharField(max_length=20, unique=True)
#     tipo = models.CharField(max_length=20, choices=TIPOS_MOVIMIENTO)
#     producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='movimientos')
#     lote = models.ForeignKey(Lote, on_delete=models.PROTECT, related_name='movimientos', null=True, blank=True)
#     cantidad = models.PositiveIntegerField()
#     precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
#     ubicacion_origen = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='movimientos_origen', null=True, blank=True)
#     ubicacion_destino = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='movimientos_destino', null=True, blank=True)
#     proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT, null=True, blank=True)
#     proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=True, blank=True)
#     documento_referencia = models.CharField(max_length=100, blank=True)
#     observaciones = models.TextField(blank=True)
#     fecha_movimiento = models.DateTimeField(auto_now_add=True)
#     usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)

#     def __str__(self):
#         return f"{self.numero} - {self.get_tipo_display()} - {self.producto.nombre}"

#     class Meta:
#         verbose_name = "Movimiento de Inventario"
#         verbose_name_plural = "Movimientos de Inventario"
#         ordering = ['-fecha_movimiento']


# # Modelo para Órdenes de Compra
# class OrdenCompra(models.Model):
#     ESTADOS = [
#         ('BORRADOR', 'Borrador'),
#         ('ENVIADA', 'Enviada'),
#         ('CONFIRMADA', 'Confirmada'),
#         ('RECIBIDA', 'Recibida'),
#         ('CANCELADA', 'Cancelada'),
#     ]

#     numero = models.CharField(max_length=20, unique=True)
#     proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
#     estado = models.CharField(max_length=20, choices=ESTADOS, default='BORRADOR')
#     fecha_orden = models.DateTimeField(auto_now_add=True)
#     fecha_entrega_estimada = models.DateField()
#     total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     observaciones = models.TextField(blank=True)
#     creado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT)

#     def __str__(self):
#         return f"OC {self.numero} - {self.proveedor.nombre}"

#     class Meta:
#         verbose_name = "Orden de Compra"
#         verbose_name_plural = "Órdenes de Compra"


# # Modelo para Detalles de Órdenes de Compra
# class DetalleOrdenCompra(models.Model):
#     orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
#     producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
#     cantidad = models.PositiveIntegerField()
#     precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
#     subtotal = models.DecimalField(max_digits=12, decimal_places=2)

#     def save(self, *args, **kwargs):
#         self.subtotal = self.cantidad * self.precio_unitario
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.orden_compra.numero} - {self.producto.nombre}"

#     class Meta:
#         unique_together = ('orden_compra', 'producto')


# # Modelo para Alertas del Sistema
# class Alerta(models.Model):
#     TIPOS_ALERTA = [
#         ('STOCK_BAJO', 'Stock Bajo'),
#         ('VENCIMIENTO', 'Próximo a Vencer'),
#         ('VENCIDO', 'Vencido'),
#         ('SISTEMA', 'Sistema'),
#     ]

#     NIVELES = [
#         ('INFO', 'Información'),
#         ('WARNING', 'Advertencia'),
#         ('ERROR', 'Error'),
#         ('CRITICAL', 'Crítico'),
#     ]

#     tipo = models.CharField(max_length=20, choices=TIPOS_ALERTA)
#     nivel = models.CharField(max_length=10, choices=NIVELES)
#     titulo = models.CharField(max_length=200)
#     mensaje = models.TextField()
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
#     lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null=True, blank=True)
#     leida = models.BooleanField(default=False)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     usuario_asignado = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return f"{self.get_tipo_display()} - {self.titulo}"

#     class Meta:
#         verbose_name = "Alerta"
#         verbose_name_plural = "Alertas"
#         ordering = ['-fecha_creacion']


# # Modelo para Auditorías de Inventario
# class AuditoriaInventario(models.Model):
#     ESTADOS = [
#         ('PLANIFICADA', 'Planificada'),
#         ('EN_PROCESO', 'En Proceso'),
#         ('COMPLETADA', 'Completada'),
#         ('CANCELADA', 'Cancelada'),
#     ]

#     codigo = models.CharField(max_length=20, unique=True)
#     nombre = models.CharField(max_length=200)
#     estado = models.CharField(max_length=20, choices=ESTADOS, default='PLANIFICADA')
#     fecha_inicio = models.DateTimeField()
#     fecha_fin = models.DateTimeField(null=True, blank=True)
#     auditor = models.ForeignKey(Usuario, on_delete=models.PROTECT)
#     observaciones = models.TextField(blank=True)

#     def __str__(self):
#         return f"Auditoría {self.codigo} - {self.nombre}"

#     class Meta:
#         verbose_name = "Auditoría de Inventario"
#         verbose_name_plural = "Auditorías de Inventario"


# # Modelo para Detalles de Auditoría
# class DetalleAuditoria(models.Model):
#     auditoria = models.ForeignKey(AuditoriaInventario, on_delete=models.CASCADE, related_name='detalles')
#     producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
#     ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
#     stock_sistema = models.PositiveIntegerField()
#     stock_fisico = models.PositiveIntegerField()
#     diferencia = models.IntegerField()
#     observaciones = models.TextField(blank=True)

#     def save(self, *args, **kwargs):
#         self.diferencia = self.stock_fisico - self.stock_sistema
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.auditoria.codigo} - {self.producto.nombre}"

#     class Meta:
#         unique_together = ('auditoria', 'producto', 'ubicacion')