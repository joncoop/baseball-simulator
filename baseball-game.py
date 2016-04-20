import random
import statistics

# options
trials = 162
verbose = False

# outcomes
WALK = 0
SINGLE = 1
DOUBLE = 2
TRIPLE = 3
HOMER = 4
OUT = 5

class Player():

    def __init__(self, name, plate_appearances, hits, doubles, triples, homers, walks):
        
        singles = hits - doubles - triples - homers

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
        self.outs = 0
        self.runs = 0
        
    def clear_bases(self):
        self.bases = [None, None, None, None]

    def show_bases(self):
        pass
    
    def advance_runners(self, result):
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
                r = random.randint(0, 100)

                if r < 15 and self.bases[3] != None:
                    output += self.bases[1].name + " advances to third. "
                    self.bases[3] = self.bases[1]
                else:
                    output += self.bases[1].name + " advances to second. "
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
                
                self.bases[1] = None
                runs += 1

            self.bases[3] = self.bases[0]

        elif result == HOMER:
            output += self.bases[0].name + " homered. "

            if self.bases[3] != None:
                output += self.bases[3].name + " scores. "
                runs += 1
                
            if self.bases[2] != None:
                output += self.bases[2].name + " scores. "
                runs += 1

            if self.bases[1] != None:
                output += self.bases[1].name + " scores. "
                runs += 1

            output += self.bases[0].name + " scores. "
            runs += 1

            self.clear_bases()
            
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
                output += self.bases[1].name + " advances to second. "
                self.bases[2] = self.bases[1]
                self.bases[1] = None

            self.bases[1] = self.bases[0]
        
        elif result == OUT:
            r1 = random.randint(0, 100)
            r2 = random.randint(0, 100)
            
            if r1 < 35:
                #ground ball
                if r2 < 60 and self.bases[1] != None and self.outs < 2:
                    output += self.bases[0].name + " grounded into a double play."
                    self.bases[1] = None
                    self.outs += 2
                elif r2 < 95:
                    output += self.bases[0].name + " grounded out."
                    self.outs += 1
                else:
                    output += self.bases[0].name + " grounded out."
                    self.outs += 1

                    if self.outs < 3:
                        if self.bases[1] != None:
                            output += self.bases[1].name + " advances to second. "
                            self.bases[2] = self.bases[1]
                            self.bases[1] = None
                            
                        if self.bases[2] != None:
                            output += self.bases[2].name + " advances to third. "
                            self.bases[3] = self.bases[2]
                            self.bases[2] = None
                            
                        if self.bases[2] != None:
                            output += self.bases[3].name + " scored. "
                            self.bases[3] = None
                            runs += 1 
            elif r1 < 70:
                # fly ball
                output += self.bases[0].name + " flied out."

                if self.outs < 2:
                    if self.bases[3] != None and r2 < 80:
                        output += self.bases[3].name + " scores on sac fly. "
                        self.bases[3] = None
                        runs += 1
                    if self.bases[2] != None and r2 < 30:
                        output += self.bases[2].name + " advanced to third. "
                        self.bases[3] = self.bases[2]
                        self.bases[2] = None

                self.outs += 1
            else:
                # strike out
                output += self.bases[0].name + " struck out."
                self.outs += 1
                
        if verbose:
            print(output)
        
        return runs
    
    def play_inning(self):
        self.outs = 0
        runs_this_inning = 0
        
        while self.outs < 3:
            self.bases[0] = self.lineup[self.batter]
            
            outcome = self.bases[0].make_plate_appearance()

            runs_this_inning += self.advance_runners(outcome)
                
            self.batter = (self.batter + 1) % 9

        if verbose:
            print("end of inning. " + str(runs_this_inning) + " runs scored.")
            print()
            
        self.runs += runs_this_inning
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

# communist DH used
#batting_order = [p1, p2, p3, p4, p5, dh, p6, p7, p8]
#batting_order = [p2, p1, p3, p4, p5, dh, p6, p7, p8]
game = Game(batting_order)

runs_scored = []

for i in range(trials):
    runs = game.simulate()
    runs_scored.append(runs)

low = min(runs_scored)
high = max(runs_scored)

mean = statistics.mean(runs_scored)
median = statistics.median(runs_scored)
mode = statistics.mode(runs_scored)
stdev = statistics.stdev(runs_scored)

print("num games: {}".format(trials))
print("min: {}".format(low))
print("max: {}".format(high))
print("mean: {}".format(mean))
print("median: {}".format(median))
print("mode: {}".format(mode))
print("standard deviation: {}".format(stdev))

'''

problems:

* scoring is too low (but only about 0.5 runs per game now)
* runners don't ever get called out when taking extra base
* no awareness of lead runner on ground ball
* runners don't replace each other on ground ball force outs

missing features:

* should runners advance additional base with two outs
  (or at least increase aggressiveness)
* speed factor
* stolen bases
* bunts

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
* does the dh make the game 'more exciting'? (or perhaps extra runs can be
  attributed to strategical differences - more conservative base running)

situational decision making:

* can code be reconfigured to test scenarios?
    - should runners push to advance extra base? if so, when?
    - when to steal
    - sacrafice bunts... worth it?

'''
