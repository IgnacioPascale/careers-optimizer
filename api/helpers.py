# Data Libraries
import pandas as pd
import numpy as np

# Helpers
from PIL import Image
import requests
import os.path
from os import listdir
from os.path import isfile, join

from data_import import elements
from models import *
import unidecode
#df, ids, roles, player_role = elements()


def printSolutionOverall(model, players, is_player):
    '''
    arg: model: gurobi model
    
    returns: solution of model
    '''
    if model.status == GRB.OPTIMAL:
        print('\nIndiviual Avg Overall: %f' % (model.objVal/players))
        print('\nPlayers:')
        print('\nName | Role | Overall')

        total_budget = 0
        total_budget_wage = 0

        for i in ids:
            if is_player[i].x == 1:
                   #unaccented_string = unidecode.unidecode(ret)
                print(unidecode.unidecode(df.loc[i, "Name"]),
                      df.loc[i, "Role"], 
                      df.loc[i, "Overall"])
                total_budget += df.loc[i, "Value"]
                total_budget_wage += df.loc[i, "Wage"]
        print("\nTotal Transfer Budget Spent: $" + str(total_budget))
        print("\nTotal Weekly Wage Budget Per Season: $" + str(total_budget_wage))
                
    else:
        print('No solution')
        
def printSolutionPotential(model, players, is_player):
    '''
    arg: model: gurobi model
    
    returns: solution of model potential
    '''
    if model.status == GRB.OPTIMAL:
        print('\nIndiviual Avg Potential: %f' % (model.objVal/players))
        print('\nPlayers:')
        print('\nName | Role | Overall | Potential')

        total_budget = 0
        total_budget_wage = 0



        for i in ids:
            if is_player[i].x == 1:
                print(unidecode.unidecode(df.loc[i, "Name"]),
                df.loc[i, "Role"], 
                df.loc[i, "Overall"],
                df.loc[i, "Potential"])
                total_budget += df.loc[i, "Value"]
                total_budget_wage += df.loc[i, "Wage"]
        print("\nTotal Transfer Budget Spent: $" + str(total_budget))
        print("\nTotal Weekly Wage Budget Per Season: $" + str(total_budget_wage))

    else:
        print('No solution')

def choosePlayers(model, is_player):
    """
    Takes names of chosen players and returns a list with the names
    
    arg: model: gurobi model
    
    
    """
    # Empty list
    list_players = []
    
    if model.status == GRB.OPTIMAL:
        for i in ids:
            if is_player[i].x == 1:
                list_players.append(i)
                
    return list_players



# Columns we want to use for statistics
stat_columns = [
    
    "Name","Age","Nationality","Overall","Value","Wage","Preferred Foot",
    "Role","Club","Work Rate",'Position', 'Height', 'Weight',
    'shooting',  'passing', 'crossing', 'heading', 'mobility',
    'defending', 'form', 'set_piece', 'goalkeeping', "Photo" ]




def dfStat(player, df):
    df_stat_temp = df[df.index == player].loc[:, stat_columns]
    return df_stat_temp


def dfStats(final_team, df):
    """
    arg: final_team: list of final team
    arg: df: Initial dataframe
    
    return: df_stat: one liner df with statistics of the player
    """
    stats_dict = {}
    
    for player in final_team:
        #df_stat_temp = df[df.index == player].loc[:, stat_columns]
        stats_dict[player] = dfStat(player, df)
        
    
    return stats_dict



def retrieveStats(player_stats):
    
    """
    Takes dataframe with player satistics and converts it into a dict
    
    arg: player_stats: df with individual player statistics
    
    return: general_stats: dict with stats
    
    """
    general_stats = {}
    stat_cols = ["Name", "Age","Club","Role", "Value","Wage", "Preferred Foot", "Work Rate", "Height", "Weight"]
    
    for col in stat_cols:
        general_stats[col] = player_stats.loc[:,col].tolist()[0]
    
    return general_stats


def saveImage(name, url):
    """
    Helper
    
    Takes url and saves the image in "images/". Only works if images was not saved before
    
    arg: name: name of the image
    arg: url: url of the image
    """
    # Name and path to be saved
    im_name = name + ".png"
    path = "images/"
    
    # Create images folder if doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')
        
    # List files in directory
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    
    # Save image if not in directory
    if im_name not in onlyfiles:
        # Open image from URL
        im = Image.open(requests.get(url, stream = True).raw)
        im.save(path+im_name)
       # print(im_name, "saved!")
        
    else:
        #print(im_name, "is already saved.")
        pass
