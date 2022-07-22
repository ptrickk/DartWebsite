from django import forms
from .models import Player
from django.db import models
from django.utils.translation import gettext_lazy as _

class CreatePlayer(forms.Form):
    username = forms.CharField(label="",help_text="Username", max_length=200, required=True, strip=True) #

class SelectGame(forms.Form):

    class GameMode(models.TextChoices):
        VS_501 = '501', _('Versus 501')
        VS_401 = '401', _('Versus 401')
        VS_301 = '301', _('Versus 301')
        RC = 'RC', _('Round the Clock')

    mode = forms.ChoiceField(label="", choices=GameMode.choices, widget=forms.Select(attrs={'class': 'form-control'}))

class CreateGame(forms.Form):
    mode = forms.CharField(max_length=3)
    player1 = forms.CharField(max_length=10)
    player2 = forms.CharField(max_length=10)
    legs = forms.IntegerField()
