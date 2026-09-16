from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from characters.models import Character
from characters.serializers import CharacterSerializer, CharacterListSerializer

CHARACTERS_URL = reverse("character:character-list")
RANDOM_CHARACTER_URL = reverse("character:character-random")


def create_chars(number_chars=10):
    Character.objects.bulk_create(
        [Character(name=f"name_{number}") for number in range(number_chars)]
    )


class CharacterListTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_characters(self):
        create_chars()
        result = self.client.get(CHARACTERS_URL)
        characters = Character.objects.all()
        serializer = CharacterListSerializer(characters, many=True)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_filter_by_name(self):
        create_chars()
        result = self.client.get(CHARACTERS_URL, {"name": "name_1"})

        for character in result.data:
            self.assertIn("name_1", character["name"].lower())

    def test_filter_returns_empty(self):
        create_chars()
        result = self.client.get(CHARACTERS_URL, {"name": "nonexistent"})

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, [])


class RandomCharacterTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_random_returns_200(self):
        create_chars()
        result = self.client.get(RANDOM_CHARACTER_URL)

        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_random_returns_valid_serializer(self):
        create_chars()
        result = self.client.get(RANDOM_CHARACTER_URL)
        char = Character.objects.get(id=result.data["id"])
        serializer = CharacterSerializer(char)

        self.assertEqual(result.data, serializer.data)

    @patch("characters.views.get_random_character")
    def test_random_with_mock(self, mock_random):
        """Мокаємо функцію щоб контролювати який персонаж повернеться"""
        chars = create_chars()
        expected_char = chars[3]  # завжди повертаємо 4-го

        # mock повертає конкретний персонаж
        mock_random.return_value = expected_char

        result = self.client.get(RANDOM_CHARACTER_URL)
        serializer = CharacterSerializer(expected_char)

        # Перевіряємо що mock викликався
        mock_random.assert_called_once()

        # Перевіряємо що повернувся саме той персонаж
        self.assertEqual(result.data, serializer.data)
        self.assertEqual(result.data["id"], expected_char.id)

    @patch("characters.views.get_random_character")
    def test_random_called_with_different_results(self, mock_random):
        """Мокаємо різні результати для кількох викликів"""
        chars = create_chars(5)

        # Кожен виклик повертає іншого персонажа
        mock_random.side_effect = [chars[0], chars[2], chars[4]]

        result_1 = self.client.get(RANDOM_CHARACTER_URL)
        result_2 = self.client.get(RANDOM_CHARACTER_URL)
        result_3 = self.client.get(RANDOM_CHARACTER_URL)

        self.assertEqual(result_1.data["id"], chars[0].id)
        self.assertEqual(result_2.data["id"], chars[2].id)
        self.assertEqual(result_3.data["id"], chars[4].id)
