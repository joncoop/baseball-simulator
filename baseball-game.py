import random

# options
trials = 1
verbose = True

# outcomes
WALK = 0
SINGLE = 1
DOUBLE = 2
TRIPLE = 3
HOMER = 4
OUT = 5


class Player():

    def __init__(self, name, plate_appearances, hits, doubles, triples, homers, walks):
        
        singles = hits - doubles - triples - homers - walks

        self.name = name
        self.walk_prob = walks / plate_appearances
        self.single_prob = singles / plate_appearances
        self.double_prob = doubles / plate_appearances
        self.triple_prob = triples / plate_appearances
        self.homer_prob = homers / plate_appearances

    def make_plate_appearance(self):
        r = random.randint(0, 1000) / 1000

        if r < self.walk_prob:
            return WALK
        elif r < self.walk_prob + self.single_prob:
            return SINGLE
        elif r < self.walk_prob + self.single_prob + self.double_prob:
            return DOUBLE
        elif r < self.walk_prob + self.single_prob + self.double_prob + self.triple_prob:
            return TRIPLE
        elif r < self.walk_prob + self.single_prob + self.double_prob + self.triple_prob + self.homer_prob:
            return HOMER
        else:
            return OUT
        

class Game():

    def __init__(self, lineup):

        self.lineup = lineup
        self.batter = 0

        self.bases = [None, None, None, None]
        self.runs = 0
        
    def clear_bases(self):
        self.bases = [None, None, None, None]

    def advance_runners(self, result, outs):
        runs = 0
        output = ""

        if result == SINGLE:
            output += self.bases[0].name + " singled. "
            
            if self.bases[3] != None:
                output += self.bases[3].name + " scores. "
                self.bases[3] = None
                runs += 1
                
            if self.bases[2] != None:
                r = random.randint(0, 100)

                if r < 60:
                    output += self.bases[2].name + " scores. "
                    runs += 1
                else:
                    output += self.bases[2].name + " advances to third. "
                    self.bases[3] = self.bases[2]
                
                self.bases[2] = None

            if self.bases[1] != None:
                output = self.bases[1].name + " advances to second. "
                self.bases[2] = self.bases[1]
                self.bases[1] = None

            self.bases[1] = self.bases[0]
            
        elif result == DOUBLE:
            output += self.bases[0].name + " doubled. "

            if self.bases[3] != None:
                output += self.bases[3].name + " scores. "
                self.bases[3] = None
                runs += 1
                
            if self.bases[2] != None:
                output += self.bases[2].name + " scores. "
                self.bases[2] = None
                runs += 1

            if self.bases[1] != None:

                r = random.randint(0, 100)

                if r < 40:
                    output += self.bases[1].name + " scores. "
                    runs += 1
                else:
                    output = self.bases[1].name + " advances to third. "
                    self.bases[3] = self.bases[1]

                self.bases[1] = None

            self.bases[2] = self.bases[0]
            
        elif result == TRIPLE:
            output += self.bases[0].name + " tripled. "

            if self.bases[3] != None:
                output += self.bases[3].name + " scores. "
                
                self.bases[3] = None
                runs += 1
                
            if self.bases[2] != None:
                output += self.bases[2].name + " scores. "
                
                self.bases[2] = None
                runs += 1

            if self.bases[1] != None:
                output += self.bases[1].name + " scores. "
                
                self.bases[2] = None
                runs += 1

            self.bases[3] = self.bases[0]

        elif result == HOMER:
            output += self.bases[0].name + " homered. "

            if self.bases[3] != None:
                output += self.bases[3].name + " scores. "
                
                self.bases[3] = None
                runs += 1
                
            if self.bases[2] != None:
                output += self.bases[2].name + " scores. "
                
                self.bases[2] = None
                runs += 1

            if self.bases[1] != None:
                output += self.bases[1].name + " scores. "
                
                self.bases[2] = None
                runs += 1

            output += self.bases[0].name + " scores. "
            self.bases[0] = None
            runs += 1
            
        elif result == WALK:
            output += self.bases[0].name + " walked. "

            if self.bases[3] != None and self.bases[2] != None and self.bases[1] != None:
                output += self.bases[3].name + " scores. "
                
                self.bases[3] = None
                runs += 1
                
            if self.bases[2] != None and self.bases[1] != None:
                output += self.bases[2].name + " advances to third. "
                
                self.bases[3] = self.bases[2]
                self.bases[2] = None

            if self.bases[1] != None:
                output = self.bases[1].name + " advances to second. "
                self.bases[2] = self.bases[1]
                self.bases[1] = None

            self.bases[1] = self.bases[0]
        
        elif result == OUT:
            output += self.bases[0].name + " got out. "

            if self.bases[3] != None and outs < 2:
                r = random.randint(0, 100)

                if r < 40:
                    output += self.bases[3].name + " scores on sac fly. "
                    
                    self.bases[3] = None
                    runs += 1
            
        if verbose:
            print(output)
        
        return runs
    
    def play_inning(self):
        outs = 0
        runs = 0
        
        while outs < 3:
            self.bases[0] = self.lineup[self.batter]
            
            outcome = self.bases[0].make_plate_appearance()
            
            if outcome == OUT:
                outs += 1

            runs += self.advance_runners(outcome, outs)
                
            self.batter = (self.batter + 1) % 9

        if verbose:
            print("end of inning. " + str(runs) + " runs scored.")
            print()
            
        self.runs += runs
        self.clear_bases()
        
    def simulate(self):
        self.runs = 0
        
        for i in range(1, 10):
            if verbose:
                print("begin inning " + str(i))
                
            self.play_inning()

        if verbose:
            print("end of game. " + str(self.runs) + " runs scored.")

        return self.runs


#2015 stats("name",       pa, hit, 2b, 3b, hr, bb)
p1 = Player("fowler",    690, 149, 29,  8, 17, 84)
p2 = Player("heyward",   610, 160, 33,  4, 13,  0)
p3 = Player("zobrist",   264,  66, 16,  1,  7, 29)
p4 = Player("rizzo",     701, 163, 38,  3, 31, 78)
p5 = Player("bryant",    650, 154, 31,  5, 26, 77)
p6 = Player("montero",   403,  86, 11,  0, 15, 49)
p7 = Player("soler",     404,  96, 18,  1, 10, 32)
p8 = Player("russell",   523, 115, 29,  1, 13, 42)
p9 = Player("arietta",    83,  12,  1,  1,  2,  1)
dh = Player("schwarber", 273,  57,  6,  1, 16, 36)
            
batting_order = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
#batting_order = [p9, p8, p7, p6, p5, p4, p3, p2, p1]
#batting_order = [p9, p3, p6, p1, p4, p8, p2, p7, p5]
#batting_order = [p4, p5, p2, p1, p3, p6, p8, p7, p9]
#batting_order = [p1, p2, p3, p4, p5, dh, p6, p7, p8]

game = Game(batting_order)

total_runs = 0

for i in range(trials):
    total_runs += game.simulate()

avg = total_runs / trials

print("num games: " + str(trials))
print("avg runs: " + str(avg))


'''

problems:

* scoring is too low
* sometimes runners should advance on out
    - sac flies
    - ground balls
* runners don't ever get called out when taking extra base

    
missing features:

* runners should advance additional base with two outs
* detect fly balls and ground balls, strike outs
    - sac flies score runner from third
    - advance on some grounders
    - advance from 1st or second on some fly balls
    - some ground balls cause double plays
    - no advance on K

* speed factor
* stolen bases

(the current simulation only predicts about half of runs actually scored.
 it's surprising how many runs these missing features actually account for.)

questions to answer:

* does it make a difference to bat pitcher 8th or 9th?
* optimal 3-4
* optimal 1-5 order
* characteristics of leadoff hitter (since it only happens once per game,
  does it even matter?)
* bunch best hitters or spread them out?
* does batting order even matter? test random orders vs traditional lineups
* how much does order matter? (runs per game, wins per season)
* how many runs equate to a "win" on average? could standings be analyzed to
  determine this?
* should runners push to advance extra base? if so, when?
* is stealing worth risk?
* when is bunting worthwhile?
* does the dh make the game 'more exciting'? (or perhaps extra runs can be
  attributed to strategical differences - more conservative base running)

probably can't be included:

* situational decision making (bunts, deliberate fly balls in sac situations, etc)

'''
