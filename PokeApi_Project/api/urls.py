from django.urls import path
from .views import ListAndCreatePokemon, DeletePokemon, EditPokemon, AdittionalPokemonViews # create_pokemon

urlpatterns = [
    path('pokemon/', ListAndCreatePokemon.as_view(), name = "create_pokemon"),
    path('enlace/<str:nombre_enlace>/<str:nombre_campo>/', ListAndCreatePokemon.filtrado, name = 'filtrado'),
    path('busqueda/',ListAndCreatePokemon.filtrado_busqueda, name = 'filtrado_search'),
    path('pokemon/<int:pk>/', EditPokemon.as_view() , name = 'edit_pokemon'), # Pide un objeto pk (primary key) si es una vista basada en clase
    path('pokemon/delete/<int:pk>', DeletePokemon.as_view(), name = 'delete_pokemon'), # pk, las vistas basadas en clases trabajan con objetos
    path('nemesis/<int:id>', AdittionalPokemonViews.nemesis_pokemon, name = 'nemesis_pokemon'),
    path('remove-tipo/', AdittionalPokemonViews.remove_pokemon, name = 'remove_pokemon'),
    path('enfrentamiento/', AdittionalPokemonViews.enfrentamiento, name = 'enfrentamiento_pokemon'),
    
    
]