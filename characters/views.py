from random import choice

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from characters.models import Character
from characters.serializers import CharacterSerializer, CharacterListSerializer


class RandomCharacterView(APIView):
    @extend_schema(
        responses={status.HTTP_200_OK: CharacterSerializer},
    )
    def get(self, request: Request) -> Response:
        """Get random character from Simpsons world"""
        pks = Character.objects.values_list("pk", flat=True)
        random_pk = choice(pks)
        random_character = Character.objects.get(pk=random_pk)
        serializer = CharacterSerializer(random_character)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterListView(generics.ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterListSerializer

    def get_queryset(self):
        queryset = self.queryset.all()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter by name insensitive to register",
                type=str,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        """list characters with filter by name"""
        return super().get(request, *args, **kwargs)
