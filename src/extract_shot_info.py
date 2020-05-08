import pandas as pd
import numpy as np
import glob
from collections import defaultdict
from pprint import pprint
from extract_game_state import game_state_extractor

pd.options.display.max_columns = 20


def shot_extractor(player_name, match_id, filepath, start_id=0):
    """
    Given a player and match name, this function extracts all shots from that match
    
    Args:
        - player_name: str, the name of the player as it appears in the data
        - match_id: int, the match id which is usually the name of the events json file
    
    Returns:
        - df_shotes: a shot dataframe
        
    """

    # define file path
    path = filepath + str(match_id) + ".json"

    # read events json into a dataframe
    df_events = pd.read_json(path)

    # initiate an empty dictionary to store shot values
    shot_dict = defaultdict(dict)

    shot_id = start_id

    goal_x1y1 = [120, 36]
    goal_x2y2 = [120, 44]

    # iterate through the events and extract shot information specific to the player
    for i in range(len(df_events)):
        try:
            if (df_events.player[i]["name"]) == player_name:
                if df_events.type[i]["name"] == "Shot":

                    freeze_frame_list = []
                    # create a new entry in the dictionary with the key being the id

                    # add event index to dictionary
                    shot_dict[shot_id]["index"] = df_events.index[i]

                    # get the game state at the event index
                    shot_dict[shot_id]["gamestate"] = game_state_extractor(
                        df_events.index[i],
                        match_id=match_id,
                        player_name=player_name,
                        filepath=filepath,
                    )

                    # reading match_id
                    shot_dict[shot_id]["match_id"] = match_id

                    shot_dict[shot_id]["start_X"] = df_events.location[i][0]

                    shot_dict[shot_id]["start_Y"] = df_events.location[i][1]
                    shot_dict[shot_id]["end_X"] = df_events.iloc[i, :]["shot"][
                        "end_location"
                    ][0]

                    shot_dict[shot_id]["end_Y"] = df_events.iloc[i, :]["shot"][
                        "end_location"
                    ][1]

                    shot_dict[shot_id]["end_Z"] = df_events.iloc[i, :]["shot"][
                        "end_location"
                    ][2]

                    # shot time
                    shot_dict[shot_id]["minute"] = df_events.minute[i]

                    # statsbomb xg information
                    shot_dict[shot_id]["statsbomb_xg"] = df_events.iloc[i, :]["shot"][
                        "statsbomb_xg"
                    ]

                    # shot body part
                    shot_dict[shot_id]["body_part"] = df_events.iloc[i, :]["shot"][
                        "body_part"
                    ]["name"]

                    # shot outcome
                    shot_dict[shot_id]["outcome"] = df_events.iloc[i, :]["shot"][
                        "outcome"
                    ]["name"]

                    # shot type
                    shot_dict[shot_id]["type"] = df_events.iloc[i, :]["shot"]["type"][
                        "name"
                    ]

                    for bool_scenario in [
                        "aerial_won",
                        "follows_dribble",
                        "first_time",
                        "open_goal",
                        "deflected",
                    ]:

                        shot_dict[shot_id][bool_scenario] = shot_exception_handler(
                            df_events, i, bool_scenario, is_boolean=True
                        )
                    # *****************************************************************************************
                    # calculate the pack density for each shot
                    # ******************************************************************************************

                    for j in range(len(df_events.iloc[i, :]["shot"]["freeze_frame"])):
                        try:
                            location = df_events.iloc[i, :]["shot"]["freeze_frame"][j][
                                "location"
                            ]
                            freeze_frame_list.append(
                                is_inside(
                                    df_events.location[i],
                                    goal_x1y1,
                                    goal_x2y2,
                                    location,
                                )
                            )
                        except KeyError:
                            freeze_frame_list.append(1)

                    shot_dict[shot_id]["pack_density"] = sum(freeze_frame_list)

                    shot_id += 1
        except:
            pass

    return shot_dict


def shot_exception_handler(
    events_df, iterator_for_row, key, is_boolean, default_return=True
):
    """
    This function checks if a key (or feature) is available for a certain shot

    Args:
        - events_df: events dataframe read from json file
        - iterator_for_row: the value for i in the main fill a list with pandas dataframes
    
    Returns:
        - True or False
    """
    # if the scenario is purely boolean return either true or false
    if is_boolean == True:
        try:
            if events_df.iloc[iterator_for_row, :]["shot"][key]:
                return True
        except KeyError:
            return False

    # else return the default_return if the scenario is not present
    else:
        try:
            if events_df.iloc[iterator_for_row, :]["shot"][key]:
                return events_df.iloc[iterator_for_row, :]["shot"][key]["name"]
        except KeyError:
            return default_return


def vectorize(pointa, pointb):
    """
    Given two points, create a vector from the first to the second
    
    Arguments:
        pointa, pointb - x,y co-ordinates (list)
    
    Returns:
        vector from point a to point b
    """
    return [pointb[0] - pointa[0], pointb[1] - pointa[1]]


def is_inside(point_shot, point_goal1, point_goal2, point_freeze):
    """
    Given the three vertices of a triangle, this function determines if a fourth
    point lies inside the triangle using the barycentric technique
    
    Reference: https://blackpawn.com/texts/pointinpoly/

    Args:
        point_shot - list, shot location x,y 
        point_goal1 and point_goal2 - list, goal edges x,y 
        point_freeze - list, player location x,y
        
    Returns:
        True or False (boolean)
    
    """
    v2 = vectorize(point_freeze, point_shot)
    v0 = vectorize(point_goal1, point_shot)
    v1 = vectorize(point_goal2, point_shot)

    u = (np.dot(v1, v1) * np.dot(v2, v0) - np.dot(v1, v0) * np.dot(v2, v1)) / (
        np.dot(v0, v0) * np.dot(v1, v1) - np.dot(v0, v1) * np.dot(v1, v0)
    )
    v = (np.dot(v0, v0) * np.dot(v2, v1) - np.dot(v0, v1) * np.dot(v2, v0)) / (
        np.dot(v0, v0) * np.dot(v1, v1) - np.dot(v0, v1) * np.dot(v1, v0)
    )

    if u < 0 or v < 0:
        return False
    elif u > 1 or v > 1:
        return False
    elif u + v > 1:
        return False
    else:
        return True


# sample_dict = shot_extractor("Vivianne Miedema", 2275062, "./sample_data/")

# pprint(sample_dict)
