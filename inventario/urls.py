from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, ProveedorViewSet, CategoriaViewSet, UbicacionViewSet,
    EtiquetaViewSet, ProductoViewSet, LoteViewSet, KitViewSet, ProyectoViewSet,
    MovimientoInventarioViewSet, OrdenCompraViewSet, AlertaViewSet, AuditoriaInventarioViewSet
)

router = DefaultRouter()

# Registro de endpoints
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'ubicaciones', UbicacionViewSet, basename='ubicacion')
router.register(r'etiquetas', EtiquetaViewSet, basename='etiqueta')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'lotes', LoteViewSet, basename='lote')
router.register(r'kits', KitViewSet, basename='kit')
router.register(r'proyectos', ProyectoViewSet, basename='proyecto')
router.register(r'movimientos', MovimientoInventarioViewSet, basename='movimiento')
router.register(r'ordenes', OrdenCompraViewSet, basename='ordencompra')
router.register(r'alertas', AlertaViewSet, basename='alerta')
router.register(r'auditorias', AuditoriaInventarioViewSet, basename='auditoria')

urlpatterns = [
    path('', include(router.urls)),
]
