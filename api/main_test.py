# Data Libraries
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt

# Math
from math import pi

# Gurobi
import gurobipy as gp
from gurobipy import GRB, quicksum

# Helpers
from PIL import Image
import requests
import os.path
from os import listdir
from os.path import isfile, join

# Imports
from helpers import *
from models import *
from plotting import *
from data_import import *

import pickle
import argparse
import sys




# Preferences
budget = 100000000#int(input("Budget to invest in $: "))
budget_wage = 800000#int(input("Maximum Weekly Wage per Season: "))
players = 2#int(input("Number of players: "))
gk = 0#int(input("Goalkeeper/s: "))
defenders = 2#int(input("Defender/s: "))
midfielders = 0#int(input("Midfielder/s: "))
attackers = 0#int(input("Attacker/s: "))
max_age = 28#int(input("Max Age: "))
max_overall =75 
df, ids, roles, player_role = elements()
# Create model - retrieve model and final variable allocation
m, is_player = createOverallModel(budget, budget_wage, players, gk, defenders, midfielders, attackers, max_age)#, max_overall)
# Optimize model (uses 'is_player')
m.optimize()
# Print Solution
#printSolutionOverall(m, players, is_player)


#pickle.dump(clf, open("./optimal_model.pkl", "wb"))

# Retrieve recommended Players
final_team = choosePlayers(m, is_player )

# Create dict with individual statistics
stats_dict = dfStats(final_team, df)

# Plot statistics
#for player in final_team:
 #  create_stats(stats_dict[player], print_plot = True)

#create_stats(stats_dict[192679], print_plot = True)
    
    
# Plot team across the Pitch
team_formation(final_team, defenders, midfielders, attackers, stats_dict)