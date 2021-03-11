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

def protocol(command: str, params):

    if command == 'overall':
        budget = params.budget if params.budget else None
        budget_wage = params.budget_wage if params.budget_wage else 200000
        gk = params.gk if params.gk else 0
        defs = params.defs if params.defs else 0
        mid = params.mid if params.mid else 0
        att = params.att if params.att else 0
        max_age = params.max_age if params.max_age else 40
        #players = params.players if params.players else (gk+defs+mid+att)
        players = gk+defs+mid+att
        #print(budget, budget_wage, players, gk, defs, mid, att, max_age)
        #if budget and budget_wage and players and gk and defs and mid and att and max_age:
        m, is_player = createOverallModel(budget, budget_wage, players, gk, defs, mid, att, max_age)
        m.optimize()
        print("SOL>>>>>>")
        print(printSolutionOverall(m, players, is_player))
        print("<<<<<<SOL")
        print('INIT>>>>>')
        print(choosePlayers(m, is_player))
        print('<<<<<END')
        return


    if command == 'potential':
        budget = params.budget if params.budget else None
        budget_wage = params.budget_wage if params.budget_wage else 200000
        gk = params.gk if params.gk else 0
        defs = params.defs if params.defs else 0
        mid = params.mid if params.mid else 0
        att = params.att if params.att else 0
        max_age = params.max_age if params.max_age else 40
        #players = params.players if params.players else (gk+defs+mid+att)
        players = gk+defs+mid+att
        max_overall = params.max_overall if params.max_overall else 80
        
        #if budget and budget_wage and players and gk and defs and mid and att and max_age and max_overall:
        m, is_player = createPotentialModel(budget, budget_wage, players, gk, defs, mid, att, max_age, max_overall)
        m.optimize()
        print("SOL>>>>>>")
        print(printSolutionPotential(m, players, is_player))
        print("<<<<<<SOL")
        print("---------")
        print('INIT>>>>>')
        print(choosePlayers(m, is_player))
        print('<<<<<END')
        return
    
    if command == 'stats':
        playerid = params.playerid if params.playerid else None
        if playerid:
            df, ids, roles, player_role = elements()
            stats = dfStat(playerid, df)
            return create_stats(stats, print_plot=False)

    if command == "formation":
        team = list(params.team.split(",")) if params.team else None
        defs = params.defs if params.defs else 0
        mid = params.mid if params.mid else 0
        att = params.att if params.att else 0

        if team:
            converted_team = [int(i) for i in team if params.team]
            df, ids, roles, player_role = elements()
            stats_dict = dfStats(converted_team, df)
            return team_formation(converted_team, defs, mid, att, stats_dict, print_plot=False)

    print("Command unknown")
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('command', metavar='C', type=str, nargs='+')
    parser.add_argument('--budget', dest='budget', nargs='?', type=int)
    parser.add_argument('--budget_wage', dest='budget_wage', nargs='?', type=int)
    #parser.add_argument('--players', dest='players', nargs='?', type=int)
    parser.add_argument('--gk', dest='gk', nargs='?', type=int)
    parser.add_argument('--defs', dest='defs', nargs='?', type=int)
    parser.add_argument('--mid', dest='mid', nargs='?', type=int)
    parser.add_argument('--att', dest='att', nargs='?', type=int)
    parser.add_argument('--max_age', dest='max_age', nargs='?', type=int)
    
    parser.add_argument('--max_overall', dest='max_overall', nargs='?', type=int)

    parser.add_argument('--playerid', dest='playerid', nargs='?', type=int)

    parser.add_argument('--team', dest='team', nargs='?', type=str)

    parsed_args = parser.parse_args()
    print(parsed_args.command)
    protocol(parsed_args.command[0], parsed_args)
    
    sys.exit(0)