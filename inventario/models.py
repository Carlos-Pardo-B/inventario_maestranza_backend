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

    # Campos existentes (mantener)
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT)
    unidad_medida = models.CharField(max_length=5, choices=UNIDADES)
    precio_promedio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Campos de stock (modificar/agregar)
    stock_fisico = models.PositiveIntegerField(default=0, verbose_name="Stock en almacén")
    stock_reservado = models.PositiveIntegerField(default=0, verbose_name="Stock reservado")
    stock_minimo = models.PositiveIntegerField(default=0, help_text="Nivel crítico - Genera alerta urgente")
    stock_regular = models.PositiveIntegerField(
        default=0, 
        help_text="Nivel de advertencia - Genera alerta preventiva",
        null=True,
        blank=True
    )
    stock_maximo = models.PositiveIntegerField(default=0, help_text="Nivel máximo deseado")
    
    # Campos adicionales
    requiere_lote = models.BooleanField(default=False)
    tiene_vencimiento = models.BooleanField(default=False)
    dias_vencimiento = models.PositiveIntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    # Propiedades calculadas
    @property
    def stock_disponible(self):
        """Stock disponible para ventas/nuevos pedidos"""
        return max(0, self.stock_fisico - self.stock_reservado)
    
    @property
    def stock_actual(self):
        """Alias para compatibilidad"""
        return self.stock_disponible
    
    @property
    def requiere_reposicion(self):
        """Indica si el producto necesita reposición"""
        return self.stock_disponible <= self.stock_minimo
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['codigo']


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

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
        ('RESERVA', 'Reserva'),
        ('CANCELACION', 'Cancelación de reserva'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='movimientos')
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    lote = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    comentario = models.TextField(blank=True)
    relacionado_con = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Actualiza el stock al guardar el movimiento"""
        es_nuevo = self._state.adding
        
        super().save(*args, **kwargs)
        
        if es_nuevo:
            self.actualizar_stock_producto()

    def actualizar_stock_producto(self):
        """Actualiza el stock físico o reservado según el tipo de movimiento"""
        if self.tipo == 'INGRESO':
            self.producto.stock_fisico += self.cantidad
        elif self.tipo == 'SALIDA':
            self.producto.stock_fisico -= self.cantidad
        elif self.tipo == 'RESERVA':
            self.producto.stock_reservado += self.cantidad
        elif self.tipo == 'CANCELACION':
            self.producto.stock_reservado -= self.cantidad
        
        self.producto.save()

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.producto.codigo} ({self.cantidad})"

    class Meta:
        verbose_name = "Movimiento de stock"
        verbose_name_plural = "Movimientos de stock"
        ordering = ['-fecha']


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

class AlertaStock(models.Model):
    NIVEL_ALERTA = [
        ('MINIMO', 'Stock Mínimo Alcanzado'),  # Solo nos interesa este nivel
    ]
    
    ESTADO_ALERTA = [
        ('PENDIENTE', 'Pendiente'),
        ('RESUELTA', 'Resuelta'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='alertas')
    nivel_alerta = models.CharField(max_length=10, choices=NIVEL_ALERTA, default='MINIMO')
    stock_actual = models.PositiveIntegerField()
    estado = models.CharField(max_length=10, choices=ESTADO_ALERTA, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='alertas_creadas'
    )
    resuelta_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alertas_resueltas'
    )
    comentarios = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Alerta de Stock Bajo'
        verbose_name_plural = 'Alertas de Stock Bajo'