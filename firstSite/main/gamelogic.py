from .models import Visit, Leg, Game, Player

def getActiveLeg(game) -> Leg:
    legs = Leg.objects.filter(game=game)

    if len(legs) == 0:  # Das erste Leg
        active_leg = Leg(game=game, number=0, winner=-1, done=False)
        active_leg.save()
        active_player = game.player1
    else:
        active_leg = Leg.objects.get(game=game, number=(len(legs) - 1))

        if active_leg.done:  # Muss ein neues Leg angefangen werden
            firstThrow = Visit.objects.get(leg=active_leg, number=0)

            if firstThrow.player == game.player1:
                active_player = game.player2
            elif firstThrow.player == game.player2:
                active_player = game.player1

            active_leg = Leg(game=game, number=(len(legs)), done=False, winner=-1)
            active_leg.save()

    return active_leg

def getActiveVisit(active_leg) -> Visit:
    visits = Visit.objects.filter(leg=active_leg)

    if len(visits) == 0:

        if len(legs) > 1:
            last_leg = Leg.objects.get(game=g, number=(active_leg.number - 1))
            prev_f_visit = Visit.objects.get(leg=last_leg, number=0)
            if prev_f_visit.player == g.player1:
                first_throw = g.player2
            else:
                first_throw = g.player1
        else:
            first_throw = g.player1

        last_visit = Visit(leg=active_leg, player=first_throw, number=0, throw1=-1)
        next_player = active_player
    else:
        last_visit = Visit.objects.get(leg=active_leg, number=(len(visits) - 1))

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