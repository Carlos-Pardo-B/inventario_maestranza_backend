from django.db.models.signals import post_save
from django.dispatch import receiver  # Esta es la importación que faltaba
from django.contrib.auth import get_user_model
from .models import Producto, AlertaStock


User = get_user_model()

@receiver(post_save, sender=Producto)
def generar_alertas_stock_bajo(sender, instance, created, **kwargs):
    """
    Genera alertas solo cuando el stock está bajo el nivel mínimo
    """
    try:
        system_user, _ = User.objects.get_or_create(
            username='sistema_alertas',
            defaults={'is_active': True, 'is_staff': False}
        )
        
        stock_actual = instance.stock_disponible
        
        # Alerta de stock MÍNIMO (crítica)
        if stock_actual <= instance.stock_minimo:
            AlertaStock.objects.update_or_create(
                producto=instance,
                nivel_alerta='MINIMO',
                estado='PENDIENTE',
                defaults={
                    'stock_actual': stock_actual,
                    'creada_por': system_user,
                    'comentarios': f'Stock bajo nivel mínimo ({stock_actual} unidades)'
                }
            )
        # Cerrar alerta si el stock se recupera
        elif stock_actual > instance.stock_minimo:
            instance.alertas.filter(estado='PENDIENTE').update(
                estado='RESUELTA',
                resuelta_por=system_user,
                comentarios='Stock superó nivel mínimo'
            )
            
    except Exception as e:
        print(f"Error al generar alertas: {str(e)}")