from django.urls import path

from characters.views import RandomCharacterView

app_name = "characters"

urlpatterns = [
    path("characters/", RandomCharacterView.as_view(), name="character-randon")
]
