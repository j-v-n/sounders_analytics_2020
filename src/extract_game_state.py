import pandas as pd
import numpy as np
import glob
from collections import defaultdict
from pprint import pprint

pd.options.display.max_columns = 20

# defining a function to extract game state given the index number for an event
def game_state_extractor(event_index, match_id, player_name, filepath):
    """ 
    Function which returns the game state at the time of an event

    Args:
        - event_index - str, The index number for the event
        - match_id - str, The match id
        - player_name - str, Name of player
        - filepath - str, Path to the events file
    
    Returns:
        - game_state - str, such as "winning by 2" or "drawing" or "losing by 1"
        
     """

    # define file path
    path = filepath + str(match_id) + ".json"

    # read events json into a dataframe
    df_events = pd.read_json(path)

    # filter the dataframe to contain only values up until and including the event index
    filt1 = df_events.index <= event_index
    df_events = df_events[filt1]

    filt2 = df_events.index <= 1
    df_starts = df_events[filt2]

    # start a goal dictionary
    goal_dict = dict()

    # extract which team the player belongs to (instead of hard-coding that Miedema plays for Arsenal)
    for _, row in df_starts.iterrows():
        if row["type"]["name"] == "Starting XI":
            for player in row["tactics"]["lineup"]:
                if player["player"]["name"] == player_name:
                    player_team_name = row["team"]["name"]

    goal_dict[player_team_name] = 0
    goal_dict["other"] = 0

    # extracting goals
    for _, row in df_events.iterrows():
        if row["type"]["name"] == "Shot":
            if row["shot"]["outcome"]["name"] == "Goal":
                if row["team"]["name"] == player_team_name:
                    goal_dict[player_team_name] += 1
                else:
                    goal_dict["other"] += 1

    # generate game state
    if goal_dict[player_team_name] > goal_dict["other"]:
        return "winning by {}".format(goal_dict[player_team_name] - goal_dict["other"])
    elif goal_dict[player_team_name] < goal_dict["other"]:
        return "losing by {}".format(goal_dict["other"] - goal_dict[player_team_name])
    else:
        return "drawing {0}-{1}".format(goal_dict[player_team_name], goal_dict["other"])
