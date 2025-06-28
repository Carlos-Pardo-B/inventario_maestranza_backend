from django.apps import AppConfig

class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventario'

    def ready(self):
        # Importa las señales solo cuando la aplicación esté completamente cargada
        # Esto evita problemas de importaciones circulares
        from . import signals  # Importación relativa