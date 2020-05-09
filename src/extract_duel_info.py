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


def duels_extractor(player_name, match_id, filepath, start_id=0):
    """
    Given a player and match name, this function extracts all duelss from that match
    
    Args:
        - player_name: str, the name of the player as it appears in the data
        - match_id: int, the match id which is usually the name of the events json file
        - filepath: str, location of files
    Returns:
        - duels_dict: dict, a duels dictionary
        
    """

    # define file path
    path = filepath + str(match_id) + ".json"

    # read events json into a dataframe
    df_events = pd.read_json(path)

    # initiate an empty dictionary to store duels values
    duels_dict = defaultdict(dict)

    duels_id = start_id

    # iterate through the events and extract duels information specific to the player
    for i in range(len(df_events)):
        try:
            if (df_events.player[i]["name"]) == player_name:
                if df_events.type[i]["name"] == "Duel":

                    # create a new entry in the dictionary with the key being the id

                    # add event index to dictionary
                    duels_dict[duels_id]["index"] = df_events.index[i + 1]

                    # get the game state at the event index
                    duels_dict[duels_id]["gamestate"] = game_state_extractor(
                        df_events.index[i + 1],
                        match_id=match_id,
                        player_name=player_name,
                        filepath=filepath,
                    )

                    # reading match_id
                    duels_dict[duels_id]["match_id"] = match_id

                    duels_dict[duels_id]["start_X"] = df_events.location[i][0]

                    duels_dict[duels_id]["start_Y"] = df_events.location[i][1]

                    duels_dict[duels_id]["type"] = df_events.duel[i]["type"]["name"]

                    duels_dict[duels_id]["outcome"] = df_events.duel[i]["outcome"][
                        "name"
                    ]

                    duels_id += 1
        except:
            pass

    return duels_dict


# def duels_exception_handler(
#     events_df, iterator_for_row, key, is_boolean, default_return=True
# ):
#     """
#     This function checks if a key (or feature) is available for a certain duels

#     Args:
#         - events_df: events dataframe read from json file
#         - iterator_for_row: the value for i in the main fill a list with pandas dataframes

#     Returns:
#         - True or False
#     """
#     # if the scenario is purely boolean return either true or false
#     if is_boolean == True:

#         if events_df.iloc[iterator_for_row, :][key].sum() != 0:
#             return False
#         else:
#             return True


# sample_dict = duels_extractor("Katie McCabe", 2275062, "./sample_data/")

# pprint(sample_dict)
