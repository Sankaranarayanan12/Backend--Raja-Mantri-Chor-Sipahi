from django.db import models

class Room(models.Model):
    room_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_started = models.BooleanField(default=False)

    def __str__(self):
        return self.room_code


class Player(models.Model):
    ROOM_ROLES = (
        ('Raja', 'Raja'),
        ('Mantri', 'Mantri'),
        ('Chor', 'Chor'),
        ('Sipahi', 'Sipahi'),
        ('None', 'None'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROOM_ROLES, default='None')
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.room.room_code}"


class Guess(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    mantri = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="mantri_guess")
    guessed_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="guessed_player")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Guess in {self.room.room_code}"
