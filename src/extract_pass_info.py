### define a function which given a particular match and player name, extracts all the relevant pass information

import pandas as pd
import numpy as np
import glob
from collections import defaultdict

pd.options.display.max_columns = 20


def pass_extractor(player_name, match_id, filepath, start_id=0):
    """
    Given a player and match name, this function extracts all passes from that match
    
    Args:
        - player_name: str, the name of the player as it appears in the data
        - match_id: int, the match id which is usually the name of the events json file
    
    Returns:
        - df_passes: a pass dataframe
    
    Issues:
        - what happens if the player is not in a match
    
    """

    # define file path
    path = filepath + str(match_id) + ".json"

    # read events json into a dataframe
    df_events = pd.read_json(path)

    # initiate an empty dictionary to store pass values
    pass_dict = defaultdict(dict)

    pass_id = start_id

    # iterate through the events and extract pass information specific to the player
    for i in range(len(df_events)):
        try:
            if (df_events.player[i]["name"]) == player_name:
                if df_events.type[i]["name"] == "Pass":
                    # create a new entry in the dictionary with the key being the id

                    # first let's read information which always appears in the dataset in the event of a pass

                    # starting with start location
                    pass_dict[pass_id]["start_location"] = df_events.location[i]

                    # end location
                    pass_dict[pass_id]["end_location"] = df_events.iloc[i, 17][
                        "end_location"
                    ]

                    # recipient information
                    pass_dict[pass_id]["recipient"] = df_events.iloc[i, 17][
                        "recipient"
                    ]["name"]

                    # pass length
                    pass_dict[pass_id]["length"] = df_events.iloc[i, 17]["length"]

                    # pass angle
                    pass_dict[pass_id]["angle"] = df_events.iloc[i, 17]["angle"]

                    # pass height
                    pass_dict[pass_id]["height_type"] = df_events.iloc[i, 17]["height"][
                        "name"
                    ]
                    # *****************************************************************************************
                    # writing a for loop to check for some scenarios which are boolean (in StatsBomb data, if the
                    # result is False, it is omitted)
                    # *****************************************************************************************

                    for bool_scenario in [
                        "backheel",
                        "deflected",
                        "miscommunication",
                        "cross",
                        "cut_back",
                        "switch",
                        "shot_assist",
                        "goal_assist",
                    ]:

                        pass_dict[pass_id][bool_scenario] = pass_exception_handler(
                            df_events, i, bool_scenario, is_boolean=True
                        )
                    # extract body part information
                    pass_dict[pass_id]["body_part"] = df_events.iloc[i, 17][
                        "body_part"
                    ]["name"]

                    # *****************************************************************************************
                    # using the exception handler to extract conditional information which is not boolean
                    # *****************************************************************************************

                    # first extracting type
                    pass_dict[pass_id]["type"] = pass_exception_handler(
                        df_events,
                        i,
                        "type",
                        is_boolean=False,
                        default_return="Regular Play",
                    )

                    # then pass outcome
                    pass_dict[pass_id]["outcome"] = pass_exception_handler(
                        df_events,
                        i,
                        "outcome",
                        is_boolean=False,
                        default_return="Completed",
                    )

                    # finally pass technique
                    pass_dict[pass_id]["technique"] = pass_exception_handler(
                        df_events,
                        i,
                        "technique",
                        is_boolean=False,
                        default_return="N/A",
                    )
                    # update pass_id for next pass
                    pass_id += 1
        except:
            pass
    return pass_dict


def pass_exception_handler(
    events_df, iterator_for_row, key, is_boolean, default_return=True
):
    """
    This function checks if a key (or feature) is available for a certain pass

    Args:
        - events_df: events dataframe read from json file
        - iterator_for_row: the value for i in the main for loop in pass_extractor
        - key: feature to be searched, like backheel, miscommunication etc

    Returns:
        - True or False
    """
    # if the scenario is purely boolean return either true or false
    if is_boolean == True:
        try:
            if events_df.iloc[iterator_for_row, 17][key]:
                return True
        except KeyError:
            return False

    # else return the default_return if the scenario is not present
    else:
        try:
            if events_df.iloc[iterator_for_row, 17][key]:
                return events_df.iloc[iterator_for_row, 17][key]["name"]
        except KeyError:
            return default_return


trial_pass = pass_extractor("Vivianne Miedema", 2275037, filepath="./sample_data/")
trial_pass_df = pd.DataFrame.from_dict(trial_pass, orient="index")
print(trial_pass_df)
