from django.contrib import admin
from .models import Usuario, Proveedor, Categoria, Ubicacion, Producto, Etiqueta, ProductoEtiqueta, Lote, Kit, ComponenteKit, Proyecto

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Proveedor)
admin.site.register(Categoria)
admin.site.register(Ubicacion)
admin.site.register(Producto)
admin.site.register(Etiqueta)
admin.site.register(ProductoEtiqueta)
admin.site.register(Lote)
admin.site.register(Kit)
admin.site.register(ComponenteKit)
admin.site.register(Proyecto)

