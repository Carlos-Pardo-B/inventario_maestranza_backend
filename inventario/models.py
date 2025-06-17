from django.db import models

# Create your models here.
class Componente(models.Model):
    nombre = models.CharField(max_length = 50)
    descripcion = models.TextField()
    numero_serie = models.IntegerField(default=0)
    ubicacion = models.TextField()
    stock = models.IntegerField(default=0)
