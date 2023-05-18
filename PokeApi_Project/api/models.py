from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Pokemon(models.Model): # Probando los verbose name en cada campo
    nombre=models.CharField("Nombre del pokemon",max_length=50)
    tipo=models.CharField("Tipo de pokemon", max_length=50)
    naturaleza=models.CharField("Naturaleza del pokemon", max_length=50)
    peso=models.IntegerField("Peso del pokemon", validators=[MinValueValidator(1), MaxValueValidator(100)])
    ataque=models.IntegerField("Ataque maximo del pokemon", validators=[MinValueValidator(1),MaxValueValidator(100)])

    class Meta:
        verbose_name="Pokemon"
        ordering = ["nombre"]
        verbose_name_plural ="Pokemones"
    def __str__(self):
        return self.nombre
    

