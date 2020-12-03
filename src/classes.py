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
        self.fill()

        self.head = head
    def fill(self):
        self.nextQ = []
        self.remainingQ = []
        self.nextValueQ = []
        self.remainingValueQ = []
        for i in range (6):
            
            self.nextQ.append( sorted(self.players, key=lambda x: x.scores[i], reverse=True))
            self.remainingQ.append(sorted(self.players, key=lambda x: sum([a*b for a, b in zip(x.scores[i:],self.discountList[:int(6-i)])]), reverse=True))
            self.nextValueQ.append(sorted(self.players, key=lambda x: (x.scores[i]/(x.price)), reverse=True))
            self.remainingValueQ.append(sorted(self.players, key=lambda x: sum([a*b for a, b in zip([y / (x.price) for y in x.scores[i:]],self.discountList[:int(6-i)])]), reverse=True))

    
    
    def branch(self, node):
        #add to children
        pass
    
    #recursive
    def selection (self, node):
        pass

    def expansion (self, node):
        pass

    def simulation (self, node):
        pass



    def monteCarlo(self, reps):
        branch(self.head)
        for i in range (reps):


        
    





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
    def __init__(self, players, bank, gameWeek, parent, score):
        #List of players
        self.players = players
        #given gameweek
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

    def verify(self):
        verify = True
        gls = 0
        defs = 0
        mids = 0
        fwds = 0
        for i in self.players:
            
            if i.position == 'Goalkeeper' :
                gls += 1
                if gls > 2:
                    verify = False

            if i.position == 'Defender':
                defs += 1
                if defs > 5:
                    verify = False
            if i.position == 'Midfielder' and mids > 5:
                mids += 1
                if mids > 5:
                    verify = False

            if i.position == 'Forward' and fwds > 3:
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
                
                

            



