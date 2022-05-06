from commons.ddd import DDDModel, DDDManager
#from models import Guest
from rest_framework import serializers
from commons.logic import *


class BoardGameManager(DDDManager):
    pass


class GameManager(DDDManager):
    pass


class GuestManager(DDDManager):

    def create(self, **kwargs):

        input_code = kwargs.get('guest_code', None)
        white_result = kwargs.pop('white_result', None)
        black_result = kwargs.pop('black_result', None)
        game = kwargs.get('game', None)
        code = game.code
        if game.winned:
            raise serializers.ValidationError("Game winned by the user, you can't continue playing.")
        if game.finished:
            raise serializers.ValidationError("Max movements reached, you can't continue playing.")
        if not checkguestformat(input_code):
            raise serializers.ValidationError('Wrong format in guest code, please try again.')
        # check if win
        if checkblacks(input_code, code) == 4:
            game.winned = True
            game.finished = True
            game.save()
        guest = self.model(white_result=checkwhites(input_code, code),
                                            black_result=checkblacks(input_code, code), **kwargs)
        # check if reach max movements
        qset = self.model.objects.filter(game=game)
        if qset.count()+1 >= game.max_guests:
            game.finished = True
            game.save()
        return guest

