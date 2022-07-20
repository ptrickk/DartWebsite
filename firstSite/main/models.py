from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Game(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player1")
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player2")
    playdate = models.DateTimeField(auto_now=True)

class Leg(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Visit(models.Model):
    leg = models.ForeignKey(Leg, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    throw1 = models.IntegerField()
    throw2 = models.IntegerField()
    throw3 = models.IntegerField()
