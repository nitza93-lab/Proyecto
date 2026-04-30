# models.py
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    # Relación uno a uno con el modelo de usuario por defecto de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Campos extendidos del perfil
    edad = models.PositiveIntegerField(null=True, blank=True)  
    genero = models.CharField(max_length=10, null=True, blank=True)  
    altura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # En cm
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)    # En kg
    tipo_diabetes = models.CharField(max_length=50, null=True, blank=True)  # Tipo 1, Tipo 2, etc.
    glucemia_promedio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # mg/dL
    enfermedades = models.TextField(null=True, blank=True)  # Renal, cardíaca, etc. (puede venir de un select en la app)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)  # Imagen subida por el usuario
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nombre_completo = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f"Perfil de {self.user.username}"



@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)



class HistorialSalud(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    fecha = models.DateTimeField(auto_now_add=True)

    glucemia = models.FloatField()
    presion_sistolica = models.FloatField()
    presion_diastolica = models.FloatField()
    ritmo_cardiaco = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.fecha}"
