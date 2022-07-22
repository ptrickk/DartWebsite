from django.urls import path
from . import views, mainPage

#SELF CREATED

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('playerlist/', views.playerlist, name='playerlist'),
    path('<int:id>', views.index, name='index'),
    path('add/', views.addPlayer, name='addPlayer'),
    path('start/', views.startGame, name='startGame'),
    path('game/', views.playGame, name='playGame')
]
