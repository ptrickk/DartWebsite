from django.urls import path
from . import views, mainPage

#SELF CREATED

urlpatterns = [
    path('sub/<int:id>', views.subpage, name='subPage'),
    path('', views.playerlist, name='playercreated'),
    path('<int:id>', views.index, name='index'),
    path('add/', views.addPlayer, name='addPlayer'),
]
