from django.db import models
from django.conf import settings
from uuid import uuid4

# Categorías de productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    codigo = models.CharField(max_length=20, unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# Ubicaciones físicas en bodega
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


# Etiquetas para clasificación
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#007bff')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    UNIDADES = [
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
    unidad_medida = models.CharField(max_length=5, choices=UNIDADES)
    precio_promedio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    stock_maximo = models.PositiveIntegerField(default=0)
    requiere_lote = models.BooleanField(default=False)
    tiene_vencimiento = models.BooleanField(default=False)
    dias_vencimiento = models.PositiveIntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def stock_actual(self):
        ingresos = self.movimientos.filter(tipo='INGRESO').aggregate(total=models.Sum('cantidad'))['total'] or 0
        salidas = self.movimientos.filter(tipo='SALIDA').aggregate(total=models.Sum('cantidad'))['total'] or 0
        return ingresos - salidas

    @property
    def requiere_reposicion(self):
        return self.stock_actual <= self.stock_minimo


class ProductoEtiqueta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'etiqueta')


class Lote(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    proveedor = models.ForeignKey('compras.Proveedor', on_delete=models.PROTECT)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad_inicial = models.PositiveIntegerField()
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Lote {self.codigo} - {self.producto.nombre}"

    @property
    def cantidad_actual(self):
        ingresos = self.movimientos.filter(tipo='INGRESO').aggregate(total=models.Sum('cantidad'))['total'] or 0
        salidas = self.movimientos.filter(tipo='SALIDA').aggregate(total=models.Sum('cantidad'))['total'] or 0
        return ingresos - salidas

    @property
    def esta_vencido(self):
        if self.fecha_vencimiento:
            from django.utils import timezone
            return timezone.now().date() > self.fecha_vencimiento
        return False


class MovimientoInventario(models.Model):
    TIPOS = [
        ('INGRESO', 'Ingreso'),
        ('SALIDA', 'Salida'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('AJUSTE', 'Ajuste'),
        ('DEVOLUCION', 'Devolución'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    numero = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='movimientos')
    lote = models.ForeignKey(Lote, on_delete=models.PROTECT, related_name='movimientos', null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    ubicacion_origen = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='movimientos_origen', null=True, blank=True)
    ubicacion_destino = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='movimientos_destino', null=True, blank=True)
    proyecto = models.ForeignKey('proyectos.Proyecto', on_delete=models.PROTECT, null=True, blank=True)
    proveedor = models.ForeignKey('compras.Proveedor', on_delete=models.PROTECT, null=True, blank=True)
    documento_referencia = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.numero} - {self.get_tipo_display()} - {self.producto.nombre}"


class Kit(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def disponible(self):
        for componente in self.componentes.all():
            if componente.producto.stock_actual < componente.cantidad:
                return False
        return True


class ComponenteKit(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name='componentes')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kit.nombre} - {self.producto.nombre} (x{self.cantidad})"

    class Meta:
        unique_together = ('kit', 'producto')
