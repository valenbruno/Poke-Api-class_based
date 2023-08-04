from .models import Pokemon
from django.db.models import Q # Q object, se utiliza para construir consultas complejas y combinar condiciones en consultas en la DB
from django.core.exceptions import FieldError
import json 
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import PokemonSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

# Camel case para clases y snake case para funciones/variables

class ListAndCreatePokemon(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self, search_query, field):
        queryset = Pokemon.objects.all()
        if search_query:
            if field: 
                field_filter = f"{field}__icontains" #icontains filtra si contiene el string ingresado dentro del string completo
                dic_field = {field_filter : search_query}
                queryset = queryset.filter(**dic_field)
            else:
                queryset = queryset.filter(
                    Q(nombre__icontains=search_query) |
                    Q(tipo__icontains=search_query) |
                    Q(naturaleza__icontains=search_query)
                )
        return queryset
    
    
    def get(self, request):
        field = request.GET.get('field')
        search_query = request.GET.get('search')
        try:
            queryset = self.get_queryset(search_query,field)
            pokemones = list(queryset.values())
            return Response({'pokemones': pokemones})
        except FieldError:
            return Response('El campo ingresado es incorrecto')

    
    def post(self, request, *args, **kwargs):
        serializer = PokemonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
        
    

class EditPokemon(APIView): 
    def put(self, request, id):
        try:
            pokemon = Pokemon.objects.get(id=id)
            serializer = PokemonSerializer(instance=pokemon,data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except Pokemon.DoesNotExist:
            return Response('No se encontro el pokemon con el id asociado', status=404)
       
class DeletePokemonAndGetID(APIView):
    def delete(self,request,id):
        try:
            pokemon = Pokemon.objects.get(id=id)
            pokemon.delete()
            return Response('Se elimino el pokemon correctamente')
        except Pokemon.DoesNotExist:
            return Response('No se encontro el pokemon con el id asociado', status=404)
    
    def get(self,request,id):
        try:
            pokemon = Pokemon.objects.get(id=id)
            serializer = PokemonSerializer(pokemon, many=False)
            return Response(serializer.data)
        except Pokemon.DoesNotExist:
            return Response('No se encontro el pokemon con el id asociado', status=404)

class AdittionalPokemonViews(APIView):
    
    @api_view(['GET'])
    def nemesis_pokemon(request,id):
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
            pokemon_dict = list(pokemon_filter.values())
            return Response({'debilidades':pokemon_dict})
        except Exception as e:
            error = e 
            print(error)
            return Response('No se encontro el Pokemon con el ID especificado', status=404) 
    
    
    @api_view(['GET','DELETE'])
    def remove_pokemon(request):
    
        tipo_pokemon = request.GET.get('tipo') # Cuando se pasa el parametro ?tipo="tipo" se lo recupera
        pokemon = Pokemon.objects.filter(tipo = tipo_pokemon)
        if not pokemon.exists():
            return Response('No se encontraron pokemones con el tipo especificado', status=404)  
        pokemon.delete()
        return Response('Se eliminaron correctamente los pokemones', status=404)
        
    @csrf_exempt
    @api_view(['POST','GET'])
    def enfrentamiento(request):
        if request.method == 'GET':
            return Response("Ingrese la informacion en formato json")
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
        try:
            data = json.loads(request.body)
            id_contendiente = data.get('pokemon1')
            id_contrincante = data.get('pokemon2')
            pokemon_contrincante = Pokemon.objects.get(id = id_contrincante)
            pokemon_contendiente = Pokemon.objects.get(id = id_contendiente)
            if(pokemon_contendiente.tipo in debilidades.get(pokemon_contrincante.tipo, [])):
                return Response('El pokemon puede ganarle a su rival')
            else:
                return Response('El pokemon no puede ganarle a su rival')
        except Pokemon.DoesNotExist:
            return Response('No existe el pokemon con el ID ingresado', status=404)    
                
        except Exception as e:
            error = e
            print(error) 
            return Response('Ocurrio un error')
        


