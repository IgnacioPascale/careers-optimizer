# Data Libraries
import pandas as pd
import numpy as np

# Gurobi
import gurobipy as gp
from gurobipy import GRB, quicksum


from data_import import *

df, ids, roles, player_role = elements()

def createOverallModel(budget, budget_wage = 500000, players = 11, gk = 1, defs = 4, mid = 4, att = 2, max_age = 40):
    """
    budget_wage = 500000,
    budget, max_wage, players, gk, defenders, midfielders, attackers, max_age)
    Creates gurobi model that maximises the Overall of players based on subject to:
        - Number of players
        - Number of gk, defenders, midfielders, attackers
        - Maximum budget
        - Maximum age
        - Maximum weekly wage for 1 season
        
    arg: budget: maximum spendable budget
    arg: wage: maximum individual wage for 1 season (gets renewed each season) - takes 500,000 as default
    arg: players: max number of players - takes 11 by default
    arg: gk: number of gk - takes 1 by default
    arg: defs: number of defenders - takes 4 by default
    arg: mid: number of midfielders - takes 4 by default
    arg: att: number of attackers - takes 2 by default
    arg: max_age: maximum individual age
    
    
    return: m: gurobi model
    """
    # Error Handling
    if (gk+defs+mid+att) != players:
        return print("Number of players do not equal the number of positions. Please try again.")
    
    # Create model
    m = gp.Model("Players Optimization")
    
    ## Add variables ##
    # Player Variable 
    is_player = m.addVars(ids, 
                          lb = 0,
                          vtype = GRB.BINARY)

    # Player/Role Variable
    is_role = m.addVars(ids, 
                        roles,
                        lb = 0,
                        vtype = GRB.BINARY)
    
    ## Add Constraints ## 
    
    # Max 11 Players Constraint
    max_players = m.addConstr( quicksum(is_player[i] for i in ids) == players)
    
    # Maximum Budget Constraint
    max_budget = m.addConstr( (quicksum(is_player[i] * df.loc[i, "Value"] for i in ids) <= budget))
    
    # Maximum Wage Constraint
    max_wage = m.addConstr( (quicksum(is_player[i] * df.loc[i, "Wage"] for i in ids) <= budget_wage))
    
    # Age Constraint
    age_upper = m.addConstrs(is_player[i] * df.loc[i, "Age"] <= max_age for i in ids)
    
    #age_lower = m.addConstr( min_age <= is_player[i]*df.loc[i, "Age"] )
    
    # Assign players position
    for i in ids:
        for role in roles:
            role_const = m.addConstr(is_role[i, role] == player_role[i, role])
    
    
    # Formation Constraint
    formation = {
        "GK" : gk,
        "DEF" : defs,
        "MID" : mid,
        "ATT" : att
    }

    # Position constraints
    for role in roles:
        m.addConstr( quicksum(is_player[i] * is_role[i, role] for i in ids) == formation[role], "Contraint "+role)
        
    
    ## Set Objective ##
    
    # Objective (Maximize overall performance)
    m.setObjective(quicksum(is_player[i]*df.loc[i, "Overall"] for i in ids), GRB.MAXIMIZE)
    
    
    return m, is_player
    
    


def createPotentialModel(budget, budget_wage = 500000, players = 11, gk = 1, defs = 4, mid = 4, att = 2, max_age = 40, max_overall = 80):
    
    """
    Creates gurobi model that maximises the Potential of players based on subject to:
        - Number of players
        - Number of gk, defenders, midfielders, attackers
        - Maximum budget
        - Maximum age
        - Maximum overall
        
    arg: budget: maximum spendable budget
    arg: players: max number of players - takes 11 by default
    arg: gk: number of gk - takes 1 by default
    arg: defs: number of defenders - takes 4 by default
    arg: mid: number of midfielders - takes 4 by default
    arg: att: number of attackers - takes 2 by default
    arg: max_age: maximum age - takes 40 by default
    arg: max_overall: maximum current overall - takes 80 by default
    
    
    return: m: gurobi model
    """
    # Error Handling
    if (gk+defs+mid+att) != players:
        return print("Number of players do not equal the number of positions. Please try again.")
    
    # Create model
    m = gp.Model("Players Potential")
    
    ## Add variables ##
    # Player Variable 
    is_player = m.addVars(ids, 
                          lb = 0,
                          vtype = GRB.BINARY)

    # Player/Role Variable
    is_role = m.addVars(ids, 
                        roles,
                        lb = 0,
                        vtype = GRB.BINARY)
    
    ## Add Constraints ## 
    
    # Max 11 Players Constraint
    max_players = m.addConstr( quicksum(is_player[i] for i in ids) == players)
    
    # Maximum Budget Constraint
    max_budget = m.addConstr( (quicksum(is_player[i] * df.loc[i, "Value"] for i in ids) <= budget))
    
    # Maximum Wage Constraint
    max_wage = m.addConstr( (quicksum(is_player[i] * df.loc[i, "Wage"] for i in ids) <= budget_wage))
    
    # Age Constraint
    age_upper = m.addConstrs(is_player[i]*df.loc[i, "Age"] <= max_age for i in ids)
    #age_lower = m.addConstr( min_age <= is_player[i]*df.loc[i, "Age"] )
    
    # Assign players position
    for i in ids:
        for role in roles:
            role_const = m.addConstr(is_role[i, role] == player_role[i, role])
    
    
    # Formation Constraint
    formation = {
        "GK" : gk,
        "DEF" : defs,
        "MID" : mid,
        "ATT" : att
    }

    # Position constraints
    for role in roles:
        m.addConstr( quicksum(is_player[i] * is_role[i, role] for i in ids) == formation[role], "Contraint "+role)
        
    
    # Max Overall Constraint
    max_overall = m.addConstr( is_player[i]*df.loc[i, "Overall"] <= max_overall)
        
    
    ## Set Objective ##
    
    # Objective (Maximize overall performance)
    m.setObjective(quicksum(is_player[i]*df.loc[i, "Potential"] for i in ids), GRB.MAXIMIZE)
    
    
    return m, is_player