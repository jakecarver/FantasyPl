import classes2
import pandas as pd
import numpy as np
import copy
import sys
df = pd.read_csv('out.csv')
initial = pd.read_csv(sys.argv[1])
players = []  
for index, row in df.iterrows():
    players.append(classes2.player(row['Name'],row['Team'],row['Position'],row['Price'],[row['1'],row['2'],row['3'],row['4'],row['5'],row['6']]))

model = classes2.game(players)

players = []  
for index, row in initial.iterrows():
    players.append(classes2.player(row['Name'],row['Team'],row['Position'],row['Price'],[row['1'],row['2'],row['3'],row['4'],row['5'],row['6']]))

var = classes2.team(players, .5, -1, None, 0,0)






#FIND WAY TO UPDATE INITIL LINEUP
#ENSURE THAT WE REACH BOTTOM OF TREE
model.monteCarlo(var, 1000, sys.argv[2])

