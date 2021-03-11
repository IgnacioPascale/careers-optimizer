# Data Libraries
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt

# Math
from math import pi

from helpers import *

from io import StringIO
import io
import base64


def create_stats(player_stats, print_plot=True):
    
    """
    For an individual dataframe of player stats, creates a radar chart with the player statistics
    
    arg: player_stats: data frame with player statistics
    return: radar_chart
    """
    
    # We do not select goalkeeping abilities for field players (we exclude last col)
    role = player_stats.loc[:, "Role"].tolist()[0]
    
    if role != "GK":
        df_temp = player_stats.iloc[:, 13:21]
    else:
        df_temp = player_stats.iloc[:, 13:22]
            
    # General Data - Retrieve stats of players
    general_stats = retrieveStats(player_stats)
    
    # List of categories (Columns 14 onwards)
    categories = list(df_temp)
    N = len(categories)
 
    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values = df_temp.values.flatten().tolist()
    values += values[:1]

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
 
    # Initialise the spider plot
    plt.figure(figsize=(20, 5))
    ax = plt.subplot(111, polar=True)
    
 
    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='grey', size=11)
 
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.ylim(0,100)
    
    # Colour dict
    
    area_colours = {"GK":"orange",
                   "DEF":"blue",
                   "MID":"green",
                   "ATT":"red"}
 
    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid', color = area_colours[role])
 
    # Fill area
    ax.fill(angles, values, area_colours[role], alpha=0.2)
    
    # Add Title
    plt.title(general_stats["Name"], size=11, color="Black", y=1.1)
    
    # Add Statistics
    # We initialize in y = 0.8 and we discount 0.05 in each iteration
    # This is done so that the text does not overlap
    init_y = 0.8
    
    for k in general_stats:
        #plt.figtext(1, init_y, "{0}: {1}".format(k, general_stats[k]) , color = "Black", fontsize=11)
        ax.text(1.2, init_y, "{0}: {1}".format(k, general_stats[k]) , color = "Black", fontsize=11, transform=ax.transAxes)
        init_y -= 0.05

    
    
    # Show the plot
    if print_plot:
        plt.show()
    else:
        byte_buffer = io.BytesIO()
        plt.savefig(byte_buffer, format='jpg')
        byte_buffer.seek(0)
        base64_data = base64.b64encode(byte_buffer.read())
        print('INIT>>>>>')
        print(base64_data)
        print('<<<<<END')

    

def team_formation(final_team, defenders, midfielders, attackers, stats_dict, print_plot=True):
    """
    Takes final team and plots the names over a football pitch
    Will only work with full teams.
    
    arg: final_team: list of players
    """
    no_players = len(final_team)
    
    # Error Handling - Only works for full teams
    if no_players - 11 != 0:
        return print("Number of players in the team is less than 11. Please try again")
        
    # Read img (Reduced size to 30%)
    x_footy = 31.75*0.3
    y_footy = 48*0.3

    img = plt.imread("footy.png")
    fig, ax = plt.subplots(figsize=(x_footy,y_footy))
    ax.axis("off")
    ax.imshow(img)

    ## Defenders
    def_y = 0.24
    
    if defenders == 5:
        def_x = 0.1
    elif defenders == 4:
        def_x = 0.2
    elif defenders == 3:
        def_x = 0.3
    elif defenders == 2:
        def_x = 0.375
    
    ## Midfielders
    mid_y = 0.43

    if midfielders == 5:
        mid_x = 0.1
    elif midfielders == 4:
        mid_x = 0.2
    elif midfielders == 3:
        mid_x = 0.3
    elif midfielders == 2:
        mid_x = 0.375
    
    ## Attackers
    att_y = 0.63

    if attackers == 5:
        att_x = 0.1
    elif attackers == 4:
        att_x = 0.2
    elif attackers == 3:
        att_x = 0.3
    elif attackers == 2:
        att_x = 0.375
        

    for p in final_team:
        temp_df = stats_dict[p]
        temp_name = temp_df.loc[:, "Name"].tolist()[0]
        temp_role = temp_df.loc[:, "Role"].tolist()[0]
        temp_overall = str(temp_df.loc[:, "Overall"].tolist()[0])
        temp_photo = temp_df.loc[:, "Photo"].tolist()[0]
        
        saveImage(str(p), temp_photo)
        path = "images/"
        im_player = plt.imread(path + str(p) + ".png")

        #plt.style.use('dark_background')
        
        if temp_role == "DEF":
            plt.figtext(def_x, def_y, temp_name, color = "Black", fontsize=14)
            plt.figtext(def_x+0.017, def_y-0.015, temp_overall, color = "Black", fontsize=14)
            img_as = fig.add_axes([def_x, def_y-0.015, 0.07, 0.07] , anchor="NE")
            img_as.imshow(im_player)
            img_as.axis('off')
            def_x += 0.175
        
    
        elif temp_role == "MID":
            plt.figtext(mid_x, mid_y, temp_name, color = "Black", fontsize=14)
            plt.figtext(mid_x+0.017, mid_y-0.015, temp_overall, color = "Black", fontsize=14)
            img_as = fig.add_axes([mid_x, mid_y-0.015, 0.07, 0.07] , anchor="NE")
            img_as.imshow(im_player)
            img_as.axis('off')
            mid_x += 0.175
        
        elif temp_role == "ATT":
            plt.figtext(att_x, att_y, temp_name, color = "Black", fontsize=14)
            plt.figtext(att_x+0.017, att_y-0.015, temp_overall, color = "Black", fontsize=14)
            img_as = fig.add_axes([att_x, att_y-0.015, 0.07, 0.07] , anchor="NE")
            img_as.imshow(im_player)
            img_as.axis('off')
            att_x += 0.175
    
        else:
            plt.figtext(0.47, 0.17, temp_name + " " + temp_overall, color = "Black", fontsize=14)
            img_as = fig.add_axes([0.47, 0.155, 0.07, 0.07] , anchor="NE")
            img_as.imshow(im_player)
            img_as.axis('off')


    # Show the plot
    if print_plot:
        plt.show()
    else:
        byte_buffer = io.BytesIO()
        plt.savefig(byte_buffer, format='jpg')
        byte_buffer.seek(0)
        base64_data = base64.b64encode(byte_buffer.read())
        print('INIT>>>>>')
        print(base64_data)
        print('<<<<<END')
        

    
