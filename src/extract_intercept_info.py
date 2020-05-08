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


def intercept_extractor(player_name, match_id, filepath, start_id=0):
    """
    Given a player and match name, this function extracts all interceptions from that match
    
    Args:
        - player_name: str, the name of the player as it appears in the data
        - match_id: int, the match id which is usually the name of the events json file
        - filepath: str, location of files
    Returns:
        - intercept_dict: an interception dictionary
        
    """

    # define file path
    path = filepath + str(match_id) + ".json"

    # read events json into a dataframe
    df_events = pd.read_json(path)

    # initiate an empty dictionary to store intercept values
    intercept_dict = defaultdict(dict)

    intercept_id = start_id

    # iterate through the events and extract    intercept information specific to the player
    for i in range(len(df_events)):
        try:
            if (df_events.player[i]["name"]) == player_name:
                if df_events.type[i]["name"] == "Interception":

                    # create a new entry in the dictionary with the key being the id

                    # add event index to dictionary
                    intercept_dict[intercept_id]["index"] = df_events.index[i + 1]

                    # get the game state at the event index
                    intercept_dict[intercept_id]["gamestate"] = game_state_extractor(
                        df_events.index[i + 1],
                        match_id=match_id,
                        player_name=player_name,
                        filepath=filepath,
                    )

                    # reading match_id
                    intercept_dict[intercept_id]["match_id"] = match_id

                    intercept_dict[intercept_id]["start_X"] = df_events.location[i][0]

                    intercept_dict[intercept_id]["start_Y"] = df_events.location[i][1]

                    intercept_dict[intercept_id]["outcome"] = df_events.iloc[i, :][
                        "interception"
                    ]["outcome"]["name"]

                    intercept_id += 1
        except:
            pass

    return intercept_dict


# sample_dict = intercept_extractor("Vivianne Miedema", 2275062, "./sample_data/")

# pprint(sample_dict)
