from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'ubicaciones', UbicacionViewSet)
router.register(r'etiquetas', EtiquetaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'producto-etiquetas', ProductoEtiquetaViewSet)
router.register(r'lotes', LoteViewSet)
router.register(r'movimientos', MovimientoInventarioViewSet)
router.register(r'kits', KitViewSet)
router.register(r'componentes-kit', ComponenteKitViewSet)
router.register(r'alertas', AlertaStockViewSet, basename='alertas')
router.register(r'productos-alertas', ProductoAlertasViewSet, basename='productos-alertas')
router.register(r'alertas-stock-bajo', AlertaStockBajoViewSet, basename='alertas-stock-bajo')

urlpatterns = [
    path('', include(router.urls)),
]
