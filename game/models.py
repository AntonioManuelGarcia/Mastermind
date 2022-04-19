from django.db import models
from django.utils import timezone
from django.conf import settings
from users.models import User


class BoardGame(models.Model):
    name = models.CharField(max_length=128, unique=True, primary_key=True, null=False, blank=False)


class Game(models.Model):
    user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE, unique=False, null=False, db_index=True
    )
    boardgame = models.ForeignKey(
        BoardGame, on_delete=models.CASCADE, unique=False, null=False, db_index=True,
        default='Mastermind'
    )
    finished = models.BooleanField(default=False)
    winned = models.BooleanField(default=False)
    max_guests = models.IntegerField(null=False, default=10)
    code = models.CharField(max_length=4, unique=False, null=False, blank=True)


class Guest(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, db_index=True)
    guest_code = models.CharField(max_length=4, unique=False, null=False, blank=False)
    white_result = models.IntegerField(null=True, default=0)
    black_result = models.IntegerField(null=True, default=0)
    create_date = models.DateTimeField(default=timezone.now, db_index=True)
