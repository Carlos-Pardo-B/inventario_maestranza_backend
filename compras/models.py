# Create your models here.
from django.db import models
from django.conf import settings
from inventario.models import Producto

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


class OrdenCompra(models.Model):
    ESTADOS = [
        ('BORRADOR', 'Borrador'),
        ('ENVIADA', 'Enviada'),
        ('CONFIRMADA', 'Confirmada'),
        ('RECIBIDA', 'Recibida'),
        ('CANCELADA', 'Cancelada'),
    ]

    numero = models.CharField(max_length=20, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='BORRADOR')
    fecha_orden = models.DateTimeField(auto_now_add=True)
    fecha_entrega_estimada = models.DateField()
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f"OC {self.numero} - {self.proveedor.nombre}"


class DetalleOrdenCompra(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.orden_compra.numero} - {self.producto.nombre}"

    class Meta:
        unique_together = ('orden_compra', 'producto')
