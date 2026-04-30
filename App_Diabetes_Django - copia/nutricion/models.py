from django.db import models
from django.contrib.auth.models import User

class RegistroComida(models.Model):
    """
    Modelo que representa un registro diario de comidas para un usuario.
    El campo foods usa JSONField para permitir flexibilidad en el contenido.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comidas")
    fecha = models.DateField(auto_now_add=True)
    foods = models.JSONField()  # Ejemplo: {"desayuno": [...], "almuerzo": [...]}

    def __str__(self):
        return f"Comida de {self.user.username} - {self.fecha}"
