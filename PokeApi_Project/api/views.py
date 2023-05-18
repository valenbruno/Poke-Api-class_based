from django.shortcuts import render,redirect
from .forms import PokemonForm
from .models import Pokemon
from django.db.models import Q # Q object, se utiliza para construir consultas complejas y combinar condiciones en consultas en la DB
from django.core.exceptions import ObjectDoesNotExist # Excepcion para la view de editar y de enfrentamiento
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, View
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET




# Create your views here.

# Camel case para clases y snake case para funciones/variables

class Inicio (TemplateView):
    template_name = 'index.html'

class ListAndCreatePokemon(CreateView, ListView):
    model = Pokemon
    form_class = PokemonForm
    context_object_name = 'pokemones'
    success_url = reverse_lazy('index')
    template_name = 'api/pokemon_list_and_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Lista de cada campo sin repetir elementos
        queryset = Pokemon.objects.values_list('nombre', flat=True)
        lista_nombre = list(set(queryset))
        queryset = Pokemon.objects.values_list('tipo', flat=True)
        lista_tipo = list(set(queryset))
        queryset = Pokemon.objects.values_list('naturaleza', flat=True)
        lista_naturaleza = list(set(queryset))
        queryset = Pokemon.objects.values_list('peso', flat=True)
        lista_peso = list(set(queryset))
        queryset = Pokemon.objects.values_list('ataque', flat=True)
        lista_ataque = list(set(queryset))

        # Agregar variables para el template
        
        context['lista_nombre'] = lista_nombre
        context['lista_tipo'] = lista_tipo
        context['lista_naturaleza'] = lista_naturaleza
        context['lista_peso'] = lista_peso
        context['lista_ataque'] = lista_ataque
        
        return context
    
    def filtrado(request, nombre_enlace, nombre_campo):
        pokemones_filtrados = Pokemon.objects.filter(**{nombre_campo: nombre_enlace})
        return render(request, 'api/filtrado.html', {'pokemones_filtrados':pokemones_filtrados, 'nombre_enlace':nombre_enlace, 'nombre_campo':nombre_campo})


    def filtrado_busqueda(request):
        parametro_busqueda = request.GET.get('q', '') # Se obtiene el contenido de la busqueda, q es la key de la barra
        if (parametro_busqueda):
            pokemones_filtrados = Pokemon.objects.filter(Q(nombre__icontains=parametro_busqueda) | Q(tipo__icontains=parametro_busqueda) 
                                                     | Q(naturaleza__icontains=parametro_busqueda))
            return render(request, 'api/filtrado.html', {'pokemones_filtrados':pokemones_filtrados, 'nombre_campo':parametro_busqueda})
        else:
            return redirect('api:create_pokemon')
        
    
# Al ser una clase lo trata todo como un objeto. Con form_class lo renderiza en el template de manera global. Lo renderiza con la palabra "form"
class EditPokemon(UpdateView): 
    model = Pokemon
    form_class = PokemonForm
    template_name = 'api/edit_pokemon.html'
    success_url = reverse_lazy('api:create_pokemon') # es como la funcion redirect pero lo hace cuando la accion se termina

class DeletePokemon(DeleteView):
    model = Pokemon
    success_url = reverse_lazy('api:create_pokemon')
    # Necesita un template como ventana de confirmacion. Por defecto busca el template: nombre_modelo_confirm_delete.html
    # Elimina directamente de la DB


class AdittionalPokemonViews(View):
    debilidades = {
                'Normal': ['Lucha'],
                'Fuego': ['Agua', 'Tierra', 'Roca'],
                'Agua': ['Planta', 'Eléctrico'],
                'Planta': ['Fuego', 'Hielo', 'Veneno', 'Volador', 'Bicho'],
                'Eléctrico': ['Tierra'],
                'Hielo': ['Fuego', 'Lucha', 'Roca', 'Acero'],
                'Lucha': ['Volador', 'Psíquico', 'Hada'],
                'Veneno': ['Tierra', 'Psíquico'],
                'Tierra': ['Agua', 'Planta', 'Hielo'],
                'Volador': ['Eléctrico', 'Hielo', 'Roca'],
                'Psíquico': ['Bicho', 'Fantasma', 'Siniestro'],
                'Bicho': ['Volador', 'Roca', 'Fuego'],
                'Roca': ['Agua', 'Planta', 'Lucha', 'Tierra', 'Acero'],
                'Fantasma': ['Fantasma', 'Siniestro'],
                'Dragón': ['Hielo', 'Dragón', 'Hada'],
                'Siniestro': ['Lucha', 'Bicho', 'Hada'],
                'Acero': ['Fuego', 'Lucha', 'Tierra'],
                'Hada': ['Veneno', 'Acero']
            } 
# No puedo acceder al diccionario global mediante self, si lo pongo primero en los argumentos me tira missing 1 required positional argument: 'request'
# Si lo pongo segundo y primero el request me tira al reves missing 1 required positional argument: 'self'
    
    @require_GET # Solo accede por solicitud HTTP GET
    def nemesis_pokemon(request,id):
        pokemon_filter = None
        error = None
        tipo = None
        debilidades = {
                'Normal': ['Lucha'],
                'Fuego': ['Agua', 'Tierra', 'Roca'],
                'Agua': ['Planta', 'Electrico'],
                'Planta': ['Fuego', 'Hielo', 'Veneno', 'Volador', 'Bicho'],
                'Electrico': ['Tierra'],
                'Hielo': ['Fuego', 'Lucha', 'Roca', 'Acero'],
                'Lucha': ['Volador', 'Psiquico', 'Hada'],
                'Veneno': ['Tierra', 'Psiquico'],
                'Tierra': ['Agua', 'Planta', 'Hielo'],
                'Volador': ['Electrico', 'Hielo', 'Roca'],
                'Psiquico': ['Bicho', 'Fantasma', 'Siniestro'],
                'Bicho': ['Volador', 'Roca', 'Fuego'],
                'Roca': ['Agua', 'Planta', 'Lucha', 'Tierra', 'Acero'],
                'Fantasma': ['Fantasma', 'Siniestro'],
                'Dragon': ['Hielo', 'Dragon', 'Hada'],
                'Siniestro': ['Lucha', 'Bicho', 'Hada'],
                'Acero': ['Fuego', 'Lucha', 'Tierra'],
                'Hada': ['Veneno', 'Acero']
            }
        try:
            pokemon = Pokemon.objects.get(id = id)
            tipo = pokemon.tipo
            pokemon_filter = Pokemon.objects.filter(tipo__in=debilidades[tipo])
        except Exception as e:
            error = e 
        return render(request, 'api/nemesis.html', {'pokemones':pokemon_filter, 'tipos':tipo, 'error':error})
    
    

    def remove_pokemon(request):
        tipo_pokemon = request.GET.get('tipo') # Cuando se pasa el parametro ?tipo="tipo" se lo recupera
        pokemon = Pokemon.objects.filter(tipo = tipo_pokemon)
        if request.method == "POST":
            pokemon.delete()
            return redirect('api:create_pokemon')
        return render(request, 'api/remove_pokemon.html', {'tipo':tipo_pokemon})

    
    def enfrentamiento(request):
        debilidades = {
                'Normal': ['Lucha'],
                'Fuego': ['Agua', 'Tierra', 'Roca'],
                'Agua': ['Planta', 'Eléctrico'],
                'Planta': ['Fuego', 'Hielo', 'Veneno', 'Volador', 'Bicho'],
                'Electrico': ['Tierra'],
                'Hielo': ['Fuego', 'Lucha', 'Roca', 'Acero'],
                'Lucha': ['Volador', 'Psíquico', 'Hada'],
                'Veneno': ['Tierra', 'Psíquico'],
                'Tierra': ['Agua', 'Planta', 'Hielo'],
                'Volador': ['Eléctrico', 'Hielo', 'Roca'],
                'Psíquico': ['Bicho', 'Fantasma', 'Siniestro'],
                'Bicho': ['Volador', 'Roca', 'Fuego'],
                'Roca': ['Agua', 'Planta', 'Lucha', 'Tierra', 'Acero'],
                'Fantasma': ['Fantasma', 'Siniestro'],
                'Dragón': ['Hielo', 'Dragón', 'Hada'],
                'Siniestro': ['Lucha', 'Bicho', 'Hada'],
                'Acero': ['Fuego', 'Lucha', 'Tierra'],
                'Hada': ['Veneno', 'Acero']
            }
        ganador = False
        error = None 
        if request.method == "POST":
            form_data = request.POST
            try:
                id_contendiente = form_data['pokemon_contendiente']
                id_contrincante = form_data['pokemon_contrincante']
                pokemon_contrincante = Pokemon.objects.get(id = id_contrincante)
                pokemon_contendiente = Pokemon.objects.get(id = id_contendiente)
                if(pokemon_contendiente.tipo in debilidades.get(pokemon_contrincante.tipo, [])):
                    ganador = True
                return render(request, 'api/ganador.html', {'ganador':ganador, 'contrincante':pokemon_contrincante, 'contendiente':pokemon_contendiente})
            except Exception as e:
                error = e 
        
        return render(request,'api/enfrentamiento.html', {'ganador':ganador, 'error':error})

