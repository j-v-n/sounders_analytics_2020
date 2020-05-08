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


def pressure_extractor(player_name, match_id, filepath, start_id=0):
    """
    Given a player and match name, this function extracts all pressures from that match
    
    Args:
        - player_name: str, the name of the player as it appears in the data
        - match_id: int, the match id which is usually the name of the events json file
        - filepath: str, location of files
    Returns:
        - df_pressures: a pressure dataframe
        
    """

    # define file path
    path = filepath + str(match_id) + ".json"

    # read events json into a dataframe
    df_events = pd.read_json(path)

    # initiate an empty dictionary to store pressure values
    pressure_dict = defaultdict(dict)

    pressure_id = start_id

    # iterate through the events and extract pressure information specific to the player
    for i in range(len(df_events)):
        try:
            if (df_events.player[i]["name"]) == player_name:
                if df_events.type[i]["name"] == "Pressure":

                    # create a new entry in the dictionary with the key being the id

                    # add event index to dictionary
                    pressure_dict[pressure_id]["index"] = df_events.index[i + 1]

                    # get the game state at the event index
                    pressure_dict[pressure_id]["gamestate"] = game_state_extractor(
                        df_events.index[i + 1],
                        match_id=match_id,
                        player_name=player_name,
                        filepath=filepath,
                    )

                    # reading match_id
                    pressure_dict[pressure_id]["match_id"] = match_id

                    pressure_dict[pressure_id]["start_X"] = df_events.location[i][0]

                    pressure_dict[pressure_id]["start_Y"] = df_events.location[i][1]

                    pressure_dict[pressure_id]["duration"] = df_events.duration[i]

                    pressure_dict[pressure_id][
                        "counterpress"
                    ] = pressure_exception_handler(
                        df_events, i, "counterpress", is_boolean=True
                    )

                    pressure_id += 1
        except:
            pass

    return pressure_dict


def pressure_exception_handler(
    events_df, iterator_for_row, key, is_boolean, default_return=True
):
    """
    This function checks if a key (or feature) is available for a certain pressure

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
