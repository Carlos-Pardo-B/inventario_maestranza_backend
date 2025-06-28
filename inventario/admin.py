from django.contrib import admin
from .models import (
    Categoria, 
    Ubicacion, 
    Etiqueta, 
    Producto, 
    ProductoEtiqueta, 
    Lote, 
    MovimientoInventario, 
    Kit, 
    ComponenteKit,
    )
# Register your models here.
admin.site.register(Categoria)
admin.site.register(Ubicacion)
admin.site.register(Etiqueta)
admin.site.register(Producto)
admin.site.register(ProductoEtiqueta)
admin.site.register(Lote)
admin.site.register(MovimientoInventario)
admin.site.register(Kit)
admin.site.register(ComponenteKit)