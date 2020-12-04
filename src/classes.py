import itertools
import random
class game:
    
    def __init__(self, head, players):
        self.players = players
        self.discount = 1
        self.discountList = []
        for i in range (6):
            self.discountList.append(self.discount^i)
        
        
        self.nextQ = []
        self.remainingQ = []
        self.nextValueQ = []
        self.remainingValueQ = []
        for i in range (6):
            
            self.nextQ.append( sorted(self.players, key=lambda x: x.scores[i], reverse=True))
            self.remainingQ.append(sorted(self.players, key=lambda x: sum([a*b for a, b in zip(x.scores[i:],self.discountList[:int(6-i)])]), reverse=True))
            self.nextValueQ.append(sorted(self.players, key=lambda x: (x.scores[i]/(x.price)), reverse=True))
            self.remainingValueQ.append(sorted(self.players, key=lambda x: sum([a*b for a, b in zip([y / (x.price) for y in x.scores[i:]],self.discountList[:int(6-i)])]), reverse=True))


        self.head = head

        self.qs = [self.nextQ,self.remainingQ, self.nextValueQ, self.remainingValueQ]
    
        
    
    #return a list of states
    def findBest(self, node, players):
        


        hit = max((len(players)-node.fts)*4, 0)
        #Positions of our n players ([Midfielder, Midfielder, Defender] for example)
        positions = []
        money = node.bank
        for i in players:
            money += i.price
            positions.append(i.position)
        #Dictionary of players for relevent positions ({Midfielder = {}, Defender = {}})
        options = {}
        #Dictionary of number of players to add for relevent positions ({Midfielder = 10, Defender = 5)
        optionsCount = {}
        for i in range(len(positions)):
            if i not in options:
                options[positions[i]] = []
                optionsCount[positions[i]] = 5
            else:
                optionsCount[positions[i]] += 5
        
        
        count = 0
        while all(value > 0 for value in optionsCount.values()):
            for q in self.qs:
                if q[node.gameWeek+1][count].position in options.keys() :
                    if q[node.gameWeek+1][count] not in options[q[node.gameWeek+1][count].position] and optionsCount[q[node.gameWeek+1][count].position] > 0:
                        options[q[node.gameWeek+1][count].position].append(q[node.gameWeek+1][count])
                        optionsCount[q[node.gameWeek+1][count].position] -= 1
        
        output = []
        curRoster = [x for x in node.players if x not in players]
        #Iterate through the first position
        for i in options[positions[0]]:
            if len(positions>1):
                for j in options[positions[1]]:
                    if len(positions>2):
                        for k in options[positions[2]]:
                            if k != j and j!= i and i!= k:
                                outList = curRoster + [i,j,k]
                                output.append(team(outList, money, node.gameWeek+1, node, node.score, node.fts))
                    else:
                        if j!= i :
                            outList = curRoster + [i,j]
                            output.append(team(outList, money, node.gameWeek+1, node, node.score, node.fts))

            else:
                
                outList = curRoster + [i]
                output.append(team(outList, money, node.gameWeek+1, node, node.score, node.fts))
        
        return output
        

        
        


        




    #keep track of fts
        
    
    def branch(self, node):
        #add to children
        branches = []
        branches.append(team(node.players, node.bank, node.gameWeek+1, node, node.score, node.fts))

        options = []
        gls = 0
        defs = 0
        mids = 0
        fwds = 0
        teamCount = {}
        for h in branches.qs:
            for i in h:
                if i.position == 'Goalkeeper' :
                    gls += 1
                    if gls < 2:
                        options.append(i)

                if i.position == 'Defender':
                    defs += 1
                    if defs <4:
                        options.append(i)
                if i.position == 'Midfielder' :
                    mids += 1
                    if mids < 3:
                        options.append(i)

                if i.position == 'Forward' :
                    fwds += 1
                    if fwds < 2:
                        options.append(i)
            
        for i in list(itertools.permutations(options,1)):
            branches += findBest(self, node, players)
        
        for i in list(itertools.permutations(options,2)):
            branches += findBest(self, node, players)

        for i in list(itertools.permutations(options,3)):
            branches += findBest(self, node, players)

        return sorted(branches, key=lambda x: x.scores[node.gameWeek+1], reverse=True)[:20]
    
    #recursive
    def selection (self, node):
        
        pass

    def expansion (self, node):
        options = self.branch(node)
        pass

    def simulation (self, node):
        pass



    def monteCarlo(self, reps):
        branch(self.head)
        

        
    





class player:
    def __init__(self, name, team, position, price, scores):
        self.name = name
        self.team = team
        self.position = position
        self.scores = scores
        self.price = price
        self.visitCount = 1
    def __hash__(self, other):
        return hash(self.name, self.team)

    def __eq__(self, other):
        return ((self.name, self.team) == (other.name, other.team))

    # def __ne__(self, other):
    #     return ((self.last, self.first) != (other.last, other.first))

    # def __lt__(self, other):
    #     return ((self.last, self.first) < (other.last, other.first))

    # def __le__(self, other):
    #     return ((self.last, self.first) <= (other.last, other.first))

    # def __gt__(self, other):
    #     return ((self.last, self.first) > (other.last, other.first))

    # def __ge__(self, other):
    #     return ((self.last, self.first) >= (other.last, other.first))

    
    def getNextScore(self, gameWeek):
        return scores[gameWeek]

    def getAveScore (self, gameWeek):
        return sum (self.scores[gameWeek]/(6-gameWeek))

    

class team:
    def __init__(self, players, bank, gameWeek, parent, score, fts):
        #List of players
        self.players = players
        #given gameweek
        self.nextQ = []
        self.remainingQ = []
        self.nextValueQ = []
        self.remainingValueQ = []
        self.fts = min(fts + 1, 2)
        

        self.gameWeek = gameWeek
        self.bank = bank
        self.starting = []
        self.keepers = []
        self.defenders = []
        self.midfielders = []
        self.forwards = []
        self.bench = []
        self.optimize()
        self.valid = self.verify()
        self.score = score + sum(i.scores[gameWeek] for i in self.starting)
        self.children = []
        self.parent = parent


        #These are ASCENDING
        self.nextQ.append( sorted(self.players, key=lambda x: x.scores[gameWeek], reverse=False))
        self.remainingQ.append(sorted(self.players, key=lambda x: sum([a*b for a, b in zip(x.scores[gameWeek:],self.discountList[:int(6-gameWeek)])]), reverse=False))
        self.nextValueQ.append(sorted(self.players, key=lambda x: (x.scores[gameWeek]/(x.price)), reverse=False))
        self.remainingValueQ.append(sorted(self.players, key=lambda x: sum([a*b for a, b in zip([y / (x.price) for y in x.scores[gameWeek:]],self.discountList[:int(6-gameWeek)])]), reverse=False))

        self.qs = [nextQ,remainingQ,nextValueQ,remainingValueQ]


    def verify(self):
        verify = True
        gls = 0
        defs = 0
        mids = 0
        fwds = 0
        teamCount = {}

        if bank < 0:
            return False
        for i in self.players:
            if i.team in teamCount:
                teamCount[i.team] += 1
                if teamCount[i.team] > 3:
                    return False
            else:
                teamCount[i.team] = 1
            
            if i.position == 'Goalkeeper' :
                gls += 1
                if gls > 2:
                    verify = False

            if i.position == 'Defender':
                defs += 1
                if defs > 5:
                    verify = False
            if i.position == 'Midfielder':
                mids += 1
                if mids > 5:
                    verify = False

            if i.position == 'Forward' :
                fwds += 1
                if fwds > 3:
                    verify = False
                

    def optimize(self):
        sortList = sorted(self.players, key=lambda x: x.scores[self.gameWeek], reverse=True)
        
        gls = 0
        defs = 0
        mids = 0
        fwds = 0

        self.starting = []
        for i in sortList:
            
            if i.position == 'Goalkeeper' and gls < 1:
                self.starting.append(i)
                gls += 1
                 

            if i.position == 'Defender' and defs < 3:
                self.starting.append(i)
                defs += 1
                

            if i.position == 'Midfielder' and mids < 2:
                self.starting.append(i)
                mids += 1
                

            if i.position == 'Forward' and fwds < 1:
                self.starting.append(i)
                fwds += 1
        count = 0
        for i in sortList:
            if i.position is not 'Goalkeeper' and count < 4 and i not in self.starting:
                count += 1
                self.starting.append(i)
            elif i not in self.starting:
                self.bench.append(i)
                
                

            



