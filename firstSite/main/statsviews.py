from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Player, Game

def gamebrowser(response):
    games = Game.objects.filter(done=True)
    dict = {"games":games}
    return render(response, "main/gamebrowser.html", dict)