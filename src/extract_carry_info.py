import pandas as pd
import numpy as np
import glob
from collections import defaultdict
from pprint import pprint
from extract_game_state import game_state_extractor
from math import atan
from math import sqrt
from math import pi

pd.options.display.max_columns = 20


def carry_extractor(player_name, match_id, filepath, start_id=0):
    """
    Given a player and match name, this function extracts all carries from that match
    
    Args:
        - player_name: str, the name of the player as it appears in the data
        - match_id: int, the match id which is usually the name of the events json file
        - filepath: str, location of files
    Returns:
        - carry_dict: dict, a dictionary of carries
        
    """

    # define file path
    path = filepath + str(match_id) + ".json"

    # read events json into a dataframe
    df_events = pd.read_json(path)

    # initiate an empty dictionary to store carry values
    carry_dict = defaultdict(dict)

    carry_id = start_id

    # iterate through the events and extract    carry information specific to the player
    for i in range(len(df_events)):
        try:
            if (df_events.player[i]["name"]) == player_name:
                if df_events.type[i]["name"] == "Carry":

                    # create a new entry in the dictionary with the key being the id

                    # add event index to dictionary
                    carry_dict[carry_id]["index"] = df_events.index[i + 1]

                    # get the game state at the event index
                    carry_dict[carry_id]["gamestate"] = game_state_extractor(
                        df_events.index[i + 1],
                        match_id=match_id,
                        player_name=player_name,
                        filepath=filepath,
                    )

                    # reading match_id
                    carry_dict[carry_id]["match_id"] = match_id

                    carry_dict[carry_id]["start_X"] = df_events.location[i][0]

                    carry_dict[carry_id]["start_Y"] = df_events.location[i][1]
                    carry_dict[carry_id]["end_X"] = df_events.iloc[i, :]["carry"][
                        "end_location"
                    ][0]

                    carry_dict[carry_id]["end_Y"] = df_events.iloc[i, :]["carry"][
                        "end_location"
                    ][1]

                    carry_dict[carry_id]["under_pressure"] = carry_exception_handler(
                        df_events, i, "under_pressure", is_boolean=True
                    )

                    carry_dict[carry_id]["angle"] = angle_calculator(
                        startX=carry_dict[carry_id]["start_X"],
                        startY=carry_dict[carry_id]["start_Y"],
                        endX=carry_dict[carry_id]["end_X"],
                        endY=carry_dict[carry_id]["end_Y"],
                    )

                    carry_dict[carry_id]["length"] = length_calculator(
                        startX=carry_dict[carry_id]["start_X"],
                        startY=carry_dict[carry_id]["start_Y"],
                        endX=carry_dict[carry_id]["end_X"],
                        endY=carry_dict[carry_id]["end_Y"],
                    )

                    carry_id += 1
        except:
            pass

    return carry_dict


def carry_exception_handler(
    events_df, iterator_for_row, key, is_boolean, default_return=True
):
    """
    This function checks if a key (or feature) is available for a certain carry

    Args:
        - events_df: events dataframe read from json file
        - iterator_for_row: the value for i in the main fill a list with pandas dataframes
    
    Returns:
        - True or False
    """
    # if the scenario is purely boolean return either true or false
    if is_boolean == True:

        if events_df.iloc[iterator_for_row, :][key].sum() == 1:
            return True
        else:
            return False


def angle_calculator(startX, startY, endX, endY):
    m1 = 0
    m2 = (endY - startY) / (endX - startX)

    angle = atan((m1 - m2) / (1 + m1 * m2))

    return -1 * angle


def length_calculator(startX, startY, endX, endY):
    length = sqrt((endX - startX) ** 2 + (endY - startY) ** 2)
    return length
