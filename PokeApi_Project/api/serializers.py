from rest_framework import serializers
from .models import Pokemon

#Convierte una estructura del modelo a JSON
class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'