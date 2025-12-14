
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Player, Guess
from .serializers import RoomSerializer
import string, random


class CreateRoomView(APIView):
    def post(self, request):
        player_name = request.data.get("name")
        if not player_name:
            return Response({"error": "Player name is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a unique 6-character room code
        while True:
            room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Room.objects.filter(room_code=room_code).exists():
                break

        # Create the room
        room = Room.objects.create(room_code=room_code)

        # Add the first player (who created the room)
        player = Player.objects.create(name=player_name, room=room)

        # Serialize and return room info
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JoinRoomView(APIView):
    def post(self, request):
        player_name = request.data.get("name")
        room_code = request.data.get("room_code")

        if not player_name or not room_code:
            return Response(
                {"error": "Player name and room_code are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if room exists
        try:
            room = Room.objects.get(room_code=room_code)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if room already has 4 players
        if room.players.count() >= 4:
            return Response(
                {"error": "Room is full (4 players already)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create player
        player = Player.objects.create(name=player_name, room=room)

        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AssignRolesView(APIView):
    def post(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        players = room.players.all()
        if players.count() != 4:
            return Response({"error": "Room must have exactly 4 players"}, status=status.HTTP_400_BAD_REQUEST)

        # Assign roles
        roles = ['Raja', 'Mantri', 'Chor', 'Sipahi']
        random.shuffle(roles)

        for player, role in zip(players, roles):
            player.role = role
            # Assign default points
            if role == 'Raja':
                player.points = 1000
            elif role == 'Mantri':
                player.points = 800
            elif role == 'Sipahi':
                player.points = 500
            else:  # Chor
                player.points = 0
            player.save()

        room.is_started = True
        room.save()

        # Return room info with updated roles
        players_data = [{"id": p.id, "name": p.name, "role": p.role, "points": p.points} for p in players]
        return Response({
            "room_code": room.room_code,
            "is_started": room.is_started,
            "players": players_data
        }, status=status.HTTP_200_OK)


class SubmitGuessView(APIView):
    def post(self, request, room_id):
        guessed_player_id = request.data.get("guessed_player_id")
        mantri_id = request.data.get("mantri_id")

        try:
            room = Room.objects.get(id=room_id)
            mantri = Player.objects.get(id=mantri_id, room=room)
            guessed_player = Player.objects.get(id=guessed_player_id, room=room)
        except (Room.DoesNotExist, Player.DoesNotExist):
            return Response({"error": "Invalid room or player"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the player making the guess is Mantri
        if mantri.role != "Mantri":
            return Response({"error": "Only Mantri can make a guess"}, status=status.HTTP_403_FORBIDDEN)

        # Save the guess
        Guess.objects.create(room=room, mantri=mantri, guessed_player=guessed_player)

        # Calculate points
        if guessed_player.role == "Chor":
            # Correct guess
            return Response({"result": "Correct! Mantri guessed the Chor."}, status=status.HTTP_200_OK)
        else:
            # Wrong guess
            return Response({"result": "Wrong! Chor steals the points."}, status=status.HTTP_200_OK)
        from rest_framework.views import APIView


class RoomResultView(APIView):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the guess for this room
        try:
            guess = Guess.objects.get(room=room)
        except Guess.DoesNotExist:
            return Response({"error": "No guess submitted yet"}, status=status.HTTP_400_BAD_REQUEST)

        mantri = guess.mantri
        chor = next(p for p in room.players.all() if p.role == "Chor")
        sipahi = next(p for p in room.players.all() if p.role == "Sipahi")

        # Update points
        if guess.guessed_player.id == chor.id:
            # Correct guess → Mantri + Sipahi keep points
            result_message = "Correct! Mantri guessed the Chor."
        else:
            # Wrong guess → Chor steals points from Mantri
            chor.points += mantri.points
            mantri.points = 0
            chor.save()
            mantri.save()
            result_message = "Wrong! Chor steals the points."

        # Prepare response
        players_data = [
            {"id": p.id, "name": p.name, "role": p.role, "points": p.points}
            for p in room.players.all()
        ]

        return Response({
            "room_code": room.room_code,
            "is_started": room.is_started,
            "result": result_message,
            "players": players_data
        }, status=status.HTTP_200_OK)
    
class LeaderboardView(APIView):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=404)

        # Get all players and sort by points descending
        players = room.players.all().order_by('-points')

        leaderboard = [
            {"id": p.id, "name": p.name, "points": p.points}
            for p in players
        ]

        return Response({
            "room_code": room.room_code,
            "leaderboard": leaderboard
        })

class NextRoundView(APIView):
    def post(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        # Reset roles for all players
        players = room.players.all()
        for p in players:
            p.role = "None"
            p.save()

        # Mark room as not started for next round
        room.is_started = False
        room.save()

        return Response({
            "message": "Next round ready. Roles reset, points retained.",
            "room_code": room.room_code,
            "players": [{"id": p.id, "name": p.name, "points": p.points, "role": p.role} for p in players]
        }, status=status.HTTP_200_OK)



