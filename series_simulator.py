import random

class Team:

    def __init__(self, name, win_pct):
        self.name = name
        self.win_pct = win_pct
        
        
def get_game_winner(team1, team2):

    
    total = 1000 * (team1.win_pct + team2.win_pct)

    n = random.randrange(0, total)

    if n < 1000 * team1.win_pct:
        return team1
    else:
        return team2


def get_series_winner(team1, team2, games):

    wins_needed = games // 2 + 1

    wins1 = 0
    wins2 = 0
    
    while wins1 < wins_needed and wins2 < wins_needed:
        winner = get_game_winner(team1, team2)

        if winner == team1:
            wins1 += 1
        else:
            wins2 += 1

    if wins1 > wins2:
        return team1
    else:
        return team2


cubs = Team("Cubs", .646)
nats = Team("Nationals", .586)



game_winner = get_game_winner(cubs, nats)
print(game_winner.name)

series_winner = get_game_winner(cubs, nats)
print(series_winner.name)


# check game percentages
trials = 1000000
cub_wins = 0
nat_wins = 0

for n in range(trials):
    game_winner = get_game_winner(cubs, nats)
    
    if game_winner == cubs:
        cub_wins += 1
    else:
        nat_wins += 1

print("cubs: " + str(cub_wins))
print("nats: " + str(nat_wins))
print("pct: " + str(cub_wins / trials))


# check series percentages
trials = 1000000
series_length = 7

cub_wins = 0
nat_wins = 0

for n in range(trials):
    series_winner = get_series_winner(cubs, nats, series_length)
    
    if series_winner == cubs:
        cub_wins += 1
    else:
        nat_wins += 1

print("cubs: " + str(cub_wins))
print("nats: " + str(nat_wins))
print("pct: " + str(cub_wins / trials))
