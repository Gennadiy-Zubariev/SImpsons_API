from django.urls import path

from characters.views import RandomCharacterView, CharacterListView

app_name = "characters"

urlpatterns = [
    path("randoom_character/", RandomCharacterView.as_view(), name="character-randon"),
    path("characters/", CharacterListView.as_view(), name="characters-list"),
]
