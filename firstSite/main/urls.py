from django.urls import path
from . import views, gameviews, statsviews

#SELF CREATED

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('playerlist/', views.playerlist, name='playerlist'),
    path('<int:id>', views.index, name='index'),
    path('add/', views.addPlayer, name='addPlayer'),
    path('start/', gameviews.startGame, name='startGame'),
    path('game/', gameviews.playGame, name='playGame'),
    path('process/', gameviews.processGame, name="processGame"),
    path('gamebrowser/', statsviews.gamebrowser, name="gameBrowser")
]
