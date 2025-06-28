from django.db import models

# Create your models here.
class Proyecto(models.Model):
    ESTADOS = [
        ('PLANIFICADO', 'Planificado'),
        ('EN_CURSO', 'En Curso'),
        ('PAUSADO', 'Pausado'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PLANIFICADO')
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()
    fecha_fin_real = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"