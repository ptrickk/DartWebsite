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

def getActiveVisit(game, active_leg) -> Visit:
    legs = Leg.objects.filter(game=game)
    visits = Visit.objects.filter(leg=active_leg)

    if len(visits) == 0:
        if len(legs) > 1:
            last_leg = Leg.objects.get(game=game, number=(active_leg.number - 1))
            prev_f_visit = Visit.objects.get(leg=last_leg, number=0)
            if prev_f_visit.player == game.player1:
                first_throw = game.player2
            else:
                first_throw = game.player1
        else:
            first_throw = game.player1

        last_visit = Visit(leg=active_leg, player=first_throw, number=0, throw1=-1)
    else:
        last_visit = Visit.objects.get(leg=active_leg, number=(len(visits) - 1))

        if last_visit.player == game.player1:
            active_player = game.player2
            next_player = game.player1
        elif last_visit.player == game.player2:
            active_player = game.player1
            next_player = game.player2

    if not last_visit.throw1 == -1:
        active_visit = Visit(leg=active_leg, player=active_player, number=len(visits), throw1=-1)
        active_visit.save()
    else:
        active_visit = last_visit

    return active_visit

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
        if not visit.throw1 == -1 and not visit.throw3 == -1:
            sum = visit.throw1 + visit.throw2 + visit.throw3
            if visit.player.id == game.player1.id:
                score1 -= sum
            elif visit.player.id == game.player2.id:
                score2 -= sum
    return [score1, score2]

def Averages(game) -> []:
    avg = [0 , 0]
    t1 = 0
    t2 = 0
    legs = Leg.objects.filter(game = game)
    for leg in legs:
        v1 = Visit.objects.filter(leg = leg, player=game.player1)
        v2 = Visit.objects.filter(leg = leg, player=game.player2)
        winner = leg.winner

        for v in v1:
            if not v.throw1 == -1:
                avg[0] += v.throw1 + v.throw2 + v.throw3
                t1 += 3

        if winner == 0:
            last = v1.pop(len(v1-1))
            if last.throw2 == 0 and last.throw3 == 0:
                t1 -= 2
            if last.throw3 == 0:
                t1 -= 1

        for v in v2:
            if not v.throw1 == -1:
                avg[1] += v.throw1 + v.throw2 + v.throw3
                t2 += 3

        if winner == 1:
            last = v2.pop(len(v1-1))
            if last.throw2 == 0 and last.throw3 == 0:
                t2 -= 2
            if last.throw3 == 0:
                t2 -= 1

    if not t1 == 0:
        avg[0] /= t1
    if not t2 == 0:
        avg[1] /= t2

    return avg