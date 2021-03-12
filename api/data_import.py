# Data Libraries
import pandas as pd
import numpy as np

def elements():

    """
    return: df, ids, roles, player_role
    """
    # Read data
    df = pd.read_csv("data/data_clean.csv", index_col = 0)

    # Create dictionaries
    player_role_temp = {}
    player_role = {}

    # Lists
    ids = list(set(df.index))
    roles = list(set(df.loc[:, "Role"]))

    for i in ids:
        # Save Values
        role = df.loc[i, "Role"]
        # Create temporary dict
        player_role_temp[i] = role


    # Fill player_role
    for i in ids:
        for role in roles:
            if player_role_temp[i] == role:
                player_role[(i, role)] = 1
            else:
                player_role[(i, role)] = 0

    return df, ids, roles, player_role