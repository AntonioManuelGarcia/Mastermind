from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .serializers import *
from .models import *
from users.models import User
from rest_framework import exceptions, permissions, status, viewsets
from django.http import HttpRequest
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings


import hashlib
import logging
import jwt
import time
import copy

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class BoardGameViewset(viewsets.ModelViewSet):
    """
    retrieve:
        Return a BoardGame instance.

    list:
        Return all BoardGames, ordered by most recently joined.

    create:
        Create a new BoardGame.

    delete:
        Remove an existing BoardGame.

    partial_update:
        Update one or more fields on an existing BoardGame.

    update:
        Update a BoardGame.
    """

    queryset = BoardGame.objects.all()
    serializer_class = BoardGameSerializer
    permission_classes = [permissions.IsAuthenticated]


class GuestViewset(viewsets.ModelViewSet):
    """
    retrieve:
        Return a Guest instance.

    list:
        Return all Guests, ordered by most recently joined.

    create:
        Create a new Guest.

    delete:
        Remove an existing Guest.

    partial_update:
        Update one or more fields on an existing Guest.

    update:
        Update a Guest.
    """

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [permissions.IsAuthenticated]


class GameViewset(viewsets.ModelViewSet):
    """
    retrieve:
        Return a user Game.

    list:
        Return all Games, ordered by most recently joined.

    create:
        Create a new Game.

    delete:
        Remove an existing Game.

    partial_update:
        Update one or more fields on an existing Game.

    update:
        Update a Game.
    """

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]