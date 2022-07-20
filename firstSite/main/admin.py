from django.contrib import admin
from .models import Player, Game, Leg, Visit
# Register your models here.

admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Leg)
admin.site.register(Visit)
