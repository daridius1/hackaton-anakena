from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PerfilUsuario(models.Model):
    """Perfil educativo del usuario - solo para tracking de valores trabajados"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Valores prioritarios que el usuario quiere trabajar
    valores_prioritarios = models.JSONField(
        default=list,
        help_text="Lista de valores educativos: ['empatía', 'honestidad', 'responsabilidad']"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
    
    def __str__(self):
        return f"Perfil de {self.user.username}"


class InteraccionSugerencia(models.Model):
    """Registra qué sugerencias eligió el usuario (para que el agente aprenda)"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interacciones')
    
    # La sugerencia
    moraleja_sugerida = models.CharField(max_length=255)
    razon_sugerencia = models.TextField(help_text="Por qué se sugirió")
    valores_cubiertos = models.JSONField(default=list)
    
    # Interacción
    fue_seleccionada = models.BooleanField(default=False)
    video_generado = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Interacción con Sugerencia"
        verbose_name_plural = "Interacciones con Sugerencias"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.moraleja_sugerida[:50]}"


# Señal para crear perfil automáticamente al registrar usuario
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea un perfil vacío cuando se registra un nuevo usuario"""
    if created:
        PerfilUsuario.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """Guarda el perfil cuando se actualiza el usuario"""
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
