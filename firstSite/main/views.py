from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Player, Game
from .forms import CreatePlayer, SelectGame

from django.contrib import messages

# Create your views here.

def index(response, id):
    user = Player.objects.get(id=id)
    dict = {"name":user.name}
    return render(response, "main/playercreated.html", dict)

def playerlist(response):
    players = Player.objects
    return render(response, "main/playerlist.html", {"players": players})

def home(response):
    return render(response, "main/home.html", {})

def startGame(response):
    if response.method == "POST":
        form = SelectGame(response.POST)
        if form.is_valid():
            mode = form.cleaned_data["mode"]
            p1 = Player.objects.get(id=response.POST.get("player1"))
            p2 = Player.objects.get(id=response.POST.get("player2"))
            g = Game(player1=p1, player2=p2,gamemode=mode)
            g.save()
    else:
        form = SelectGame()
    players = Player.objects.all()
    dict = {"form":form, "players":players}
    return render(response, "main/start.html", dict)

def addPlayer(response):
    if response.method == "POST":
        form = CreatePlayer(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            p = Player(name = n)
            p.save()
            return HttpResponseRedirect("/%i" %p.id)
    else:
        form = CreatePlayer()
    dict = {"form":form}
    return render(response, "main/addplayer.html", dict)
