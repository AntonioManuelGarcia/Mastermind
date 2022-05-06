from rest_framework import serializers
from . import models
from rest_framework.validators import UniqueValidator
#from commons.logic import *


class BoardGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BoardGame
        fields = "__all__"


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guest
        fields = "__all__"

    # def create(self, validated_data):
    #     print('kwargs')
    #     print(validated_data)
    #     try:
    #         return checktocreateguest(validated_data)
    #     except Exception as err:
    #         raise err


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
