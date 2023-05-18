from django import forms
from .models import Pokemon

class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        extra_field = forms.CharField(max_length=50)
        fields = ['nombre','tipo','naturaleza','peso','ataque'] # Labels predefinidos con el verbose_name del models
        labels = {
            'nombre' : 'Nombre del pokemon' # con la variable label se le puede cambiar los nombres a los labels
        }
        widgets = {
            'nombre' : forms.TextInput(attrs = {'placeholder': 'Ingrese el nombre del pokemon', 'class': 'form-control'}), # class si se usaria bs por ej
        # se puede hacer para todos los campos del modelo      
            'tipo' : forms.TextInput(attrs= {'placeholder': 'Ingrese el tipo del pokemon'}),
            'naturaleza' : forms.TextInput(attrs= {'placeholder': 'Ingrese la naturaleza del pokemon'}),
            'peso' : forms.TextInput(attrs= {'placeholder': 'Ingrese el peso del pokemon'}),
            'ataque' : forms.TextInput(attrs= {'placeholder': 'Ingrese el ataque del pokemon'}),

        }
