from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Player, Game, Leg, Visit
from .forms import CreatePlayer, SelectGame, CreateGame, LogVisit


def startGame(response):
    if response.method == "POST":
        form = CreateGame(response.POST)
        if form.is_valid():
            mode = form.cleaned_data["mode"]  # Part of SelectGame-Class
            p1 = Player.objects.get(id=form.cleaned_data["player1"])  # Not Part of SelectGame
            p2 = Player.objects.get(
                id=form.cleaned_data["player2"])  # Not Part of SelectGame    response.POST.get("player2")
            legs = form.cleaned_data["legs"]
            g = Game(player1=p1, player2=p2, gamemode=mode, legs=legs)
            g.save()
            response.session['g_id'] = g.id
            return HttpResponseRedirect("/game")
    else:
        form = SelectGame()
    players = Player.objects.all()
    dict = {"form": form, "players": players}
    return render(response, "main/start.html", dict)


def playGame(response):
    dict = {"valid": 0}
    if 'g_id' in response.session:
        newleg = 0

        g_id = response.session['g_id']
        if g_id != -1:
            g = Game.objects.get(id=g_id)
            legs = Leg.objects.filter(game=g)

            if len(legs) == 0:  # Das erste Leg
                active_leg = Leg(game=g, number=0, winner=-1, done=False)
                active_leg.save()
                active_player = g.player1
            else:
                active_leg = Leg.objects.get(game=g, number=(len(legs)-1))

                if active_leg.done: #Muss ein neues Leg angefangen werden
                    firstThrow = Visit.objects.get(leg=active_leg, number=0)

                    if firstThrow.player == g.player1:
                        active_player = g.player2
                    elif firstThrow.player == g.player2:
                        active_player = g.player1

                    active_leg = Leg(game=g, number=(len(legs)), done=False, winner=-1)
                    active_leg.save()
                else: #Leg ist noch nicht zuende
                    active_player = g.player1 #DEBUG

            #Active Leg is defined

            visits = Visit.objects.filter(leg=active_leg)
            scores = Scores(visits, g, 501)

            if len(visits) == 0:

                if len(legs) > 1:
                    last_leg = Leg.objects.get(game=g, number=(active_leg.number-1))
                    prev_f_visit = Visit.objects.get(leg=last_leg, number = 0)
                    if prev_f_visit.player == g.player1:
                        first_throw = g.player2
                    else:
                        first_throw = g.player1
                else:
                    first_throw = g.player1

                last_visit = Visit(leg=active_leg, player=first_throw, number=0, throw1=-1)
                next_player = active_player
            else:
                last_visit = Visit.objects.get(leg=active_leg, number=(len(visits)-1))

                if last_visit.player == g.player1:
                    active_player = g.player2
                    next_player = g.player1
                elif last_visit.player == g.player2:
                    active_player = g.player1
                    next_player = g.player2

            if not last_visit.throw1 == -1:
                active_visit = Visit(leg=active_leg, player=active_player, number=len(visits), throw1=-1)
                active_visit.save()
            else:
                active_visit = last_visit
                active_player = active_visit.player

            #Active Visit & Player defined

            # Neues Visit verarbeiten
            if response.method == "POST":
                form = LogVisit(response.POST)
                if form.is_valid():
                    active_visit.throw1 = form.cleaned_data["throw1"]
                    active_visit.throw2 = form.cleaned_data["throw2"]
                    active_visit.throw3 = form.cleaned_data["throw3"]

                    if active_player == g.player1:
                        pid = 0
                    else:
                        pid = 1

                    scores = Scores(visits, g, 501)
                    score = scores[pid] - (active_visit.throw1 + active_visit.throw2 + active_visit.throw3)

                    if score < 0:
                        active_visit.throw1 = 0
                        active_visit.throw2 = 0
                        active_visit.throw3 = 0
                    elif score == 0:
                        active_leg.winner = pid
                        active_leg.done = True
                        active_leg.save()
                        newleg = 1
                    scores[pid] = scores[pid] - (active_visit.throw1 + active_visit.throw2 + active_visit.throw3)

                    active_visit.done = True
                    active_visit.save()

            visits = Visit.objects.filter(leg=active_leg)
            legs = Leg.objects.filter(game=g)
            scores = Scores(visits, g, 501)
            standing = Standings(legs, g)

            #SET CORRECT NEXT PLAYER
            if len(visits) > 0 and newleg == 0:
                last_visit = Visit.objects.get(leg=active_leg, number=(len(visits)-1))
                if last_visit.throw1 == -1:
                    next_player = last_visit.player
                else:
                    if last_visit.player == g.player1:
                        next_player = g.player2
                    else:
                        next_player = g.player1
            if newleg == 1:
                if active_leg.winner == 0:
                    next_player = g.player1
                else:
                    next_player = g.player2

            #GAME IS OVER
            if standing[0] == g.legs:
                g.winner = 0
                g.done = True
                g.save()
                next_player = g.player1 #for win screen
                done = 1
                response.session['g_id'] = -1
            elif standing[1] == g.legs:
                g.winner = 1
                g.done = True
                g.save()
                next_player = g.player2#for win screen
                response.session['g_id'] = -1
                done = 1
            else:
                done = 0

            dict = {"game": g, "valid": 1, "player":next_player, "score": scores, "visits": visits, "newleg":newleg, "standing": standing, "done":done}
    else:
        dict = {"valid": 0}
    return render(response, "main/game.html", dict)

def Standings(legs, game) -> []:
    wins = [0,0]
    for leg in legs:
        if leg.done:
            wins[leg.winner] += 1

    return wins

def Scores(visits, game, goal) -> []:
    score1 = goal
    score2 = goal
    for visit in visits:
        if not visit.throw1 == -1:
            sum = visit.throw1 + visit.throw2 + visit.throw3
            if visit.player.id == game.player1.id:
                score1 -= sum
            elif visit.player.id == game.player2.id:
                score2 -= sum
    return [score1, score2]
