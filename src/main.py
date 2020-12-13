import classes
import pandas as pd
import numpy as np
import copy

df = pd.read_csv('out.csv')
players = []  
for index, row in df.iterrows():
    players.append(classes.player(row['Name'],row['Team'],row['Position'],row['Price'],[row['1'],row['2'],row['3'],row['4'],row['5'],row['6']]))

model = classes.game(players)

teamList = []

gkpCount = 0
fwdCount = 0
midCount = 0
defCount = 0
totalCount = 0
for i in model.nextQ[0]:
    
    if i.position == 'Goalkeeper' and gkpCount < 2:
        gkpCount+=1
        teamList.append(copy.copy(i))
        totalCount += 1

    elif i.position == 'Defender' and defCount < 5:
        defCount+=1
        teamList.append(copy.copy(i))
        totalCount += 1

    elif i.position == 'Midfielder' and midCount < 5:
        midCount+=1
        teamList.append(copy.copy(i))
        totalCount += 1

    elif i.position == 'Forward' and fwdCount < 3:
        fwdCount+=1
        teamList.append(copy.copy(i))
        totalCount += 1
    
    elif totalCount ==15:
        break
        

var = classes.team(teamList, .5, 0, None, 0,0)
print("STARTERS")
for i in var.starting:

    print(i.name)
    print(i.position)
    print(i.scores[0])


print("BENCH")

for i in var.bench:

    print(i.name)
    print(i.position)
    print(i.scores[0])

#FIND WAY TO UPDATE INITIL LINEUP
#ENSURE THAT WE REACH BOTTOM OF TREE
model.monteCarlo(var, 3)
