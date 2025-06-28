from django.contrib import admin
from .models import (
    Proveedor,
    OrdenCompra,
    DetalleOrdenCompra
)
# Register your models here.
admin.site.register(Proveedor)
admin.site.register(OrdenCompra)
admin.site.register(DetalleOrdenCompra)