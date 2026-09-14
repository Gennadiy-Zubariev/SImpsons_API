import time

import requests
from django.conf import settings

from characters.models import Character


def scrape_characters() -> list[Character]:
    next_url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL
    characters = []
    while next_url_to_scrape is not None:
        response = requests.get(next_url_to_scrape)

        if response.status_code == 429:
            print("Rate limited, waiting 5 seconds...")
            time.sleep(5)
            continue

        if not response.ok:
            break

        characters_response = response.json()

        for character_dict in characters_response["results"]:
            characters.append(
                Character(
                    api_id=character_dict["id"],
                    name=character_dict["name"],
                    status=character_dict["status"],
                    species=character_dict["species"],
                    gender=character_dict["gender"],
                    image=character_dict["image"],
                )
            )
        next_url_to_scrape = characters_response["info"]["next"]

    return characters


def save_characters(characters: list[Character]) -> None:
    Character.objects.bulk_create(characters, ignore_conflicts=True)


def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)
