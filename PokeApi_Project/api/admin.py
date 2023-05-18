from django.contrib import admin
from .models import Pokemon
from import_export import resources # de la libreria Django import / export
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class PokemonResource(resources.ModelResource): # Se pueden exportar e importar las instancias de los metodos
    class Meta:
        model = Pokemon

class PokemonAdmin(ImportExportModelAdmin, admin.ModelAdmin): # ImportExportModelAdmin debe ir primero en la lista de parametros asi tiene prioridad
    list_display=('nombre','tipo','naturaleza','peso','ataque') # Identificadores en el panel de administracion
    search_fields = ['nombre'] # Barra de busqueda en el panel de administracion. Filtra solo por nombre
    resource_class = PokemonResource

admin.site.register(Pokemon,PokemonAdmin)