from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Game(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player1")
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player2")
    gamemode = models.CharField(max_length=15, default="none")
    playdate = models.DateTimeField(auto_now=True, blank=True)
    legs = models.IntegerField(blank=True)
    done = models.BooleanField(default=False, blank=True)
    winner = models.IntegerField(default=-1, blank=True)

class Leg(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    number = models.IntegerField()
    done = models.BooleanField(default=False)
    winner = models.IntegerField(default=-1)

class Visit(models.Model):
    leg = models.ForeignKey(Leg, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    number = models.IntegerField()
    throw1 = models.IntegerField(default=0)
    throw2 = models.IntegerField(default=0)
    throw3 = models.IntegerField(default=0)
    done = models.BooleanField(default=False)
