from django.contrib import admin
from .models import Usuario, Proveedor, Categoria

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Proveedor)
admin.site.register(Categoria)

