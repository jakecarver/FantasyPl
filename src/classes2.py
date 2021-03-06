import itertools
import random
import math
import numpy
import pandas as pd
import csv
import copy
'''
BASE CLASS:

Decay Rate: 1

UCB Buffer: 5
'''


class game:
    
    def __init__(self,  players):
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


        self.head = None

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
        

        fts = min(node.fts+1-len(players),2)
        #Dictionary of players for relevent positions ({Midfielder = {}, Defender = {}})
        options = {}
        #Dictionary of number of players to add for relevent positions ({Midfielder = 10, Defender = 5)
        optionsCount = {}
        
        for i in positions:
            if i not in options:
                options[i] = []
                optionsCount[i] = 5
            else:
                optionsCount[i] += 5
        
        
        count = 0
        
        #Choosing best potential trades
        while all(value > 0 for value in optionsCount.values()):
            
            for q in self.qs:
                if q[node.gameWeek+1][count].position in options.keys() :
                    #Check if statement
                    if q[node.gameWeek+1][count] not in options[q[node.gameWeek+1][count].position] and optionsCount[q[node.gameWeek+1][count].position] > 0  and q[node.gameWeek+1][count] not in node.players:
                        options[q[node.gameWeek+1][count].position].append(q[node.gameWeek+1][count])
                        optionsCount[q[node.gameWeek+1][count].position] -= 1
                        if not all(value > 0 for value in optionsCount.values()):
                            break
                count+=1
        
        output = []
        curRoster = [x for x in node.players if x not in players]
        
        #Iterate through the first position
        for i in options[positions[0]]:
            if len(positions)>1:
                for j in options[positions[1]]:
                    if len(positions)>2:
                        for k in options[positions[2]]:
                            if k != j and j!= i and i!= k:
                                
                                outList = curRoster + [i,j,k]
                                newTeam = team(outList, money-k.price-j.price-i.price, node.gameWeek+1, node, node.score-hit, fts)
                                if newTeam.verify():
                                    
                                    output.append(newTeam)
                    else:
                        if j!= i :
                            outList = curRoster + [i,j]
                            newTeam = team(outList, money-i.price-j.price, node.gameWeek+1, node, node.score-hit, fts)
                            if newTeam.verify():
                                    
                                output.append(newTeam)
            else:
                outList = curRoster + [i]
                newTeam = team(outList, money-i.price, node.gameWeek+1, node, node.score-hit, fts)
                if newTeam.verify():
                                    
                    output.append(newTeam)
        
        return output
        

        
        


        




    #keep track of fts
        
    
    def branch(self, node):
        #add to children
        branches = []

        #ADDS THE NO TRADE BRANCH
        branches.append(team(node.players, node.bank, node.gameWeek+1, node, node.score, node.fts))
        #print("GAMEWEEK: ",node.gameWeek)
        #for i in node.players:

        #    print(i.name, "---",i.position,"---",i.scores[node.gameWeek])
        options = []
        gls = 0
        defs = 0
        mids = 0
        fwds = 0
        teamCount = {}
        for i in range (15):
            #Fix later
            for j in branches[0].qs:
                #print("Length: ", len(j))
                #print(i)
                #print (j)
                
                if j[i].position == 'Goalkeeper' and j[i] not in options:
                    gls += 1
                    if gls < 2:
                        options.append(j[i])

                if j[i].position == 'Defender' and j[i] not in options:
                    defs += 1
                    if defs <4:
                        options.append(j[i])
                if j[i].position == 'Midfielder' and j[i] not in options:
                    mids += 1
                    if mids < 3:
                        options.append(j[i])

                if j[i].position == 'Forward' and j[i] not in options:
                    fwds += 1
                    if fwds < 2:
                        options.append(j[i])
            
        for i in list(itertools.permutations(options,1)):
            branches += self.findBest(node, i)
        
        for i in list(itertools.permutations(options,2)):
            branches += self.findBest(node, i)

        for i in list(itertools.permutations(options,3)):
            branches += self.findBest(node, i)
        
        saveList = sorted(branches, key=lambda x: x.score, reverse=True)[:20]

        saveList = sorted(saveList, key=lambda x: x.UCB, reverse=True)
        
        return saveList
    
    def expansion(self, node):
        if node.gameWeek != 5 and node.gameWeek != 4:
            node.children = self.branch(node)
            #New Addition
        elif node.gameWeek == 4:
            node.children = [sorted(self.branch(node), key=lambda x: x.score, reverse=True)[0]]
        

    #recursive
    def selection (self, node):
        if len(node.children) == 0:
            
            return node
        node.children = sorted(node.children, key=lambda x: x.UCB, reverse=True)
        return self.selection(node.children[0])
        

    

    def simulation (self, node):
        if node.gameWeek == 5:
            return node.score
        random.seed()
        
        nextList = self.branch(node)
        rand = random.randint(0, len(nextList)-1)
        nextNode = nextList[rand]
        return self.simulation(nextNode)

    

    def backProp (self, node, score):
        node.update(score)
        if node.parent == None:
            return
        
        #Fill function next time
        self.backProp(node.parent, score)

    def monteCarlo(self, head, reps, name):
        
        self.head = head
        bests = []
        scores = []
        for i in range (reps):
            leaf = self.selection(self.head)
            self.expansion(leaf)
            score = self.simulation(leaf)
            print(score)
            self.backProp(leaf, score)

            if leaf.parent is not None:
                print ("REP: ",i,"--- BEST: ",self.head.best, "--- LEVEL: ", leaf.gameWeek,"--- PARENT UCB: ", leaf.parent.UCB)
            else: 
                print ("REP: ",i,"--- BEST: ",self.head.best, "--- LEVEL: ", leaf.gameWeek)

            #Evolution of the best all time score
            bests.append([head.best])

            #Most recent best
            scores.append([leaf.best])
        with open(name+"bests.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(bests)
        with open(name+"scores.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(scores)
        cur = self.head
        

        rosters = []

        thisRoster = []
        print("INITIAL PLAYERS")
        for i in cur.players:

            print(i.name)
            thisRoster.append(i.name)
            print(i.position)
            print(i.scores[0])
        rosters.append(copy.copy(thisRoster))
        while len(cur.children)>0:
            thisRoster = []
            cur = sorted(cur.children, key=lambda x: x.best, reverse=True)[0]
            #-1 FOR SOME REASON
            print(cur.best)
            print("GAMEWEEK: ",cur.gameWeek)
            print("Starting: ")
            for i in cur.starting:

                print(i.name, "---",i.team,"---",i.position,"---",i.scores[cur.gameWeek])
                thisRoster.append(i.name)

            print("Bench: ")
            for i in cur.bench:
                print(i.name, "---",i.team,"---",i.position,"---",i.scores[cur.gameWeek])
                thisRoster.append(i.name)

            rosters.append(copy.copy(thisRoster))

        with open(name+"rosters.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rosters)
            
        return cur
        
        

        
    





class player:
    def __init__(self, name, team, position, price, scores):
        self.name = name
        self.team = team
        self.position = position
        self.scores = scores
        self.price = price
        self.visitCount = 1
    def __hash__(self):
        return hash(self.name + self.team)

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

        self.discount = 1
        self.discountList = []
        for i in range (6):
            self.discountList.append(self.discount^i)
        
        self.visits = 0
        self.runningMean = 9999
        self.best = -1
        self.UCB = 9999
        self.bias = 1

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
        if gameWeek > -1:
            self.score = score + sum(i.scores[gameWeek] for i in self.starting)
        else:
            self.score = 0
        self.children = []
        self.parent = parent


        self.nextQ = []
        self.remainingQ = []
        self.nextValueQ = []
        self.remainingValueQ = []

        #These are ASCENDING
        self.nextQ  =sorted(self.players, key=lambda x: x.scores[gameWeek], reverse=False)
        self.remainingQ= sorted(self.players, key=lambda x: sum([a*b for a, b in zip(x.scores[gameWeek:],self.discountList[:int(6-gameWeek)])]), reverse=False)
        self.nextValueQ =sorted(self.players, key=lambda x: (x.scores[gameWeek]/(x.price)), reverse=False)
        self.remainingValueQ=sorted(self.players, key=lambda x: sum([a*b for a, b in zip([y / (x.price) for y in x.scores[gameWeek:]],self.discountList[:int(6-gameWeek)])]), reverse=False)

        self.qs = [self.nextQ,self.remainingQ,self.nextValueQ,self.remainingValueQ]

    def update(self, newScore):
        if self.runningMean == 9999:
            self.runningMean = newScore
            self.visits = 1
        else:
            self.visits += 1
            self.runningMean = ((self.runningMean*(self.visits-1))+newScore)/self.visits
        
        

        if self.parent is not None and self.visits > 5 and self.UCB != -1:
            self.UCB = self.runningMean + (self.bias*math.sqrt(numpy.log(self.parent.visits+1)/self.visits))
        
        
        #experiment with
        else:
            if len(self.children) > 0:
                sortBest = sorted(self.children, key=lambda x: x.UCB, reverse=True)[0]
                if sortBest == -1:
                    UCB = -1
                self.UCB = self.runningMean + 6-self.visits
            else:
                self.UCB = self.runningMean + 6-self.visits
        if newScore>self.best:
            self.best = newScore


    def verify(self):
        
        gls = 0
        defs = 0
        mids = 0
        fwds = 0
        teamCount = {}

        if self.bank < 0:
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
                    return False

            if i.position == 'Defender':
                defs += 1
                if defs > 5:
                    return False
            if i.position == 'Midfielder':
                mids += 1
                if mids > 5:
                    return False

            if i.position == 'Forward' :
                fwds += 1
                if fwds > 3:
                    return False
        return True
                

    def optimize(self):
        if self.gameWeek == -1:
            return
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
                
                

            



