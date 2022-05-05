from rest_framework import serializers
from . import models
from rest_framework.validators import UniqueValidator
from commons.logic import *


class BoardGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BoardGame
        fields = "__all__"


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guest
        fields = "__all__"

    def create(self, validated_data):
        input_code = validated_data.get('guest_code', None)
        white_result = validated_data.pop('white_result', None)
        black_result = validated_data.pop('black_result', None)
        game = validated_data.get('game', None)
        code = game.code
        #print(game)
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
        guest = models.Guest.objects.create(white_result=checkwhites(input_code, code),
                                            black_result=checkblacks(input_code, code), **validated_data)
        # check if reach max movements
        qset = models.Guest.objects.filter(game=game)
        if qset.count() >= game.max_guests:
            game.finished = True
            game.save()
        return guest


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = "__all__"

    def to_representation(self, instance):
        """override representation to return game_type data not only id"""
        ret = super().to_representation(instance)
        qset = models.Guest.objects.filter(game=instance)
        ret['guests'] = [GuestSerializer(m).data for m in qset]
        ret['code'] = ""
        return ret

    def create(self, validated_data):
        input_code = validated_data.pop('code', None)
        winned = validated_data.pop('winned', None)
        game = models.Game.objects.create(code=createcode(), winned=False, **validated_data)
        return game
