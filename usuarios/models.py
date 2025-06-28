from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrador del Sistema'),
        ('GESTOR_INV', 'Gestor de Inventario'),
        ('COMPRADOR', 'Comprador'),
        ('LOGISTICA', 'Encargado de Logística'),
        ('JEFE_PROD', 'Jefe de Producción'),
        ('AUDITOR', 'Auditor de Inventario'),
        ('GERENTE_PROY', 'Gerente de Proyectos'),
        ('USUARIO_FINAL', 'Usuario Final/Trabajador de Planta'),
    ]

    rol = models.CharField(max_length=20, choices=ROLES, default='USUARIO_FINAL')
    telefono = models.CharField(max_length=15, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
