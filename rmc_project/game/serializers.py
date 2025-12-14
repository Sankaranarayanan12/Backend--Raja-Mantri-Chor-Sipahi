from rest_framework import serializers
from .models import Room, Player, Guess
    
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'role', 'points']


class RoomSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_code', 'created_at', 'is_started', 'players']


class GuessSerializer(serializers.ModelSerializer):
    mantri = PlayerSerializer(read_only=True)
    guessed_player = PlayerSerializer(read_only=True)

    class Meta:
        model = Guess
        fields = ['id', 'room', 'mantri', 'guessed_player', 'created_at']
