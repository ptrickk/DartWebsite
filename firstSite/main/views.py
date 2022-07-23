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


