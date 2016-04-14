import random

class Player():

    def __init__(self, name, plate_appearances, hits, doubles, triples, homers, walks):
        self.name = name
        self.singles = hits - doubles - triples - homers - walks
        self.doubles = doubles
        self.triples = triples
        self.homers = homers
        self.walks = walks
        self.plate_appearances = plate_appearances

        
class Game():

    def __init__(self, lineup, verbose = False):

        self.lineup = lineup
        self.batter = 0

        self.bases = [0, 0, 0]
        self.runs = 0

        self.verbose = verbose
        
    def clear_bases(self):
        self.bases = [0, 0, 0]

    def advance_runners(self, num_bases):
        runs = 0
        
        if num_bases == 1:
            runs += self.bases[2]
            self.bases[2] = self.bases[1]
            self.bases[1] = self.bases[0]
            self.bases[0] = 1
        elif num_bases == 2:
            runs += self.bases[1] + self.bases[2]
            self.bases[2] = self.bases[0]
            self.bases[1] = 1
            self.bases[0] = 0
        elif num_bases == 3:
            runs += self.bases[0] + self.bases[1] + self.bases[2]
            self.bases[2] = 1
            self.bases[1] = 0
            self.bases[0] = 0
        elif num_bases >= 4:
            runs += 1 + self.bases[0] + self.bases[1] + self.bases[2]
            self.clear_bases()

        if self.verbose:
            print("runners advance " + str(num_bases) + " bases. " + str(runs) + " runs scored.")
            print(self.bases)
        
        return runs
    
    def play_inning(self):
        outs = 0
        runs = 0
        
        while outs < 3:
            current_hitter = self.lineup[self.batter]
            
            single_prob = current_hitter.singles / current_hitter.plate_appearances
            
            double_prob = current_hitter.doubles / current_hitter.plate_appearances
            double_prob += single_prob
            
            triple_prob = current_hitter.triples / current_hitter.plate_appearances
            triple_prob += double_prob
            
            homer_prob = current_hitter.homers / current_hitter.plate_appearances
            homer_prob += triple_prob
            
            walk_prob = current_hitter.walks / current_hitter.plate_appearances
            walk_prob += homer_prob
            
            r = random.randint(0, 1000) / 1000

            if r < single_prob:
                outcome = current_hitter.name + " singled."
                bases_to_advance = 1
            elif r < double_prob:
                outcome = current_hitter.name + " doubled."
                bases_to_advance = 2
            elif r < triple_prob:
                outcome = current_hitter.name + " tripled."
                bases_to_advance = 3
            elif r < homer_prob:
                outcome = current_hitter.name + " homered."
                bases_to_advance = 4
            elif r < walk_prob:
                outcome = current_hitter.name + " walked."
                bases_to_advance = 1
            else:
                outcome = current_hitter.name + " is out."
                outs += 1
                bases_to_advance = 0

            if bases_to_advance > 0:                    
                runs += self.advance_runners(bases_to_advance)

            if self.verbose:
                print(outcome)
                
            self.batter = (self.batter + 1) % 9

        if self.verbose:
            print("end of inning. " + str(runs) + " runs scored.")
            print()
            
        self.runs += runs
        self.clear_bases()
        
    def simulate(self):
        self.runs = 0
        
        for i in range(1, 10):
            if self.verbose:
                print("begin inning " + str(i))
                
            self.play_inning()

        if self.verbose:
            print("end of game. " + str(self.runs) + " runs scored.")

        return self.runs


#2015 stats("name",     pa, hit, 2b, 3b, hr, bb)
p1 = Player("fowler",  690, 149, 29,  8, 17, 84)
p2 = Player("heyward", 610, 160, 33,  4, 13,  0)
p3 = Player("zobrist", 264,  66, 16,  1,  7, 29)
p4 = Player("rizzo",   701, 163, 38,  3, 31, 78)
p5 = Player("bryant",  650, 154, 31,  5, 26, 77)
p6 = Player("montero", 403,  86, 11,  0, 15, 49)
p7 = Player("soler",   404,  96, 18,  1, 10, 32)
p8 = Player("russell", 523, 115, 29,  1, 13, 42)
p9 = Player("arietta",  83,  12,  1,  1,  2,  1)

batting_order = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
#batting_order = [p9, p8, p7, p6, p5, p4, p3, p2, p1]
#batting_order = [p9, p3, p6, p1, p4, p8, p2, p7, p5]

game = Game(batting_order, False)

total_runs = 0
trials = 10000

for i in range(trials):
    total_runs += game.simulate()

avg = total_runs / trials

print("num games: " + str(trials))
print("avg runs: " + str(avg))


'''
assumptions:

* runners advance same number of bases as hit

problems:

* scoring is too low
* runners should only advance on walk with force
* sometimes runners should advance on out
    - sac flies
    - ground balls
    
missing features:

* runners should advance additional base with two outs
* score runner from 2nd on single, or make probability based
  (speed included in probability)
* advance runner from first to third on single, probability based
* detect fly balls and ground balls, strike outs
    - sac flies score runner from third
    - advance on some grounders
    - ground balls cause double plays
    - no advance on K

* speed factor
* stolen bases

(the current simulation only predicts about half of runs actually scored.
 it's surprising how many runs these missing features actually account for.)

questions to answer:

* does it make a difference to bat pitcher 8th or 9th?
* optimal 3-4
* optimal 1-5 order
* bunch best hitters or spread them out?
* does batting order even matter? test random orders vs lineups
* how much does order matter? (runs per game, wins per season)
* how many runs equate to a "win" on average? could standings be analyzed to
  determine this?
* should runners push to advance extra base? if so, when?
* is stealing worth risk?

probably can't be included:

* situational decision making

'''
