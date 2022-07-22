from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Player, Game
from .forms import CreatePlayer, SelectGame, CreateGame

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
        form = CreateGame(response.POST)
        if form.is_valid():
            mode = form.cleaned_data["mode"]                        #Part of SelectGame-Class
            p1 = Player.objects.get(id=form.cleaned_data["player1"])#Not Part of SelectGame
            p2 = Player.objects.get(id=form.cleaned_data["player2"])#Not Part of SelectGame    response.POST.get("player2")
            legs = form.cleaned_data["legs"]
            g = Game(player1=p1, player2=p2,gamemode=mode, legs=legs)
            g.save()
            response.session['g_id'] = g.id
            return HttpResponseRedirect("/game")
    else:
        form = SelectGame()
    players = Player.objects.all()
    dict = {"form":form, "players":players}
    return render(response, "main/start.html", dict)

def addPlayer(response):
    if response.method == "POST":
        form = CreatePlayer(response.POST)
        if form.is_valid() == True:
            n = form.cleaned_data["username"]
            p = Player(name = n)
            p.save()
            return HttpResponseRedirect("/%i" %p.id)
    else:
        form = CreatePlayer()
    dict = {"form":form}
    return render(response, "main/addplayer.html", dict)

def playGame(response):
    if 'g_id' in response.session:
        g_id = response.session['g_id']
        if g_id != -1:
            g = Game(id=g_id)
            dict = {"game":g, "valid": 1}
        else:
            dict = {}
    else:
        dict = {"valid": 0}
    return render(response, "main/game.html", dict)
