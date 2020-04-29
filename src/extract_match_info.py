import pandas as pd
import numpy as np
import glob
from collections import defaultdict


def match_extractor(
    filepath="/home/jayanth/Documents/statsbomb/april_2020_data/open-data-master/data/matches/",
    competitions=["37", "49", "72"],
    team="Arsenal WFC",
):
    """
    Given a list of seasons and a team, this function extracts match metadata
    
    Args:
        - filepath : location of match metadata files (not events data)
        - competitions: list of str, competition ids
        - team: str, team name
    
    Returns:
        - match_dict: match metadata dictionary
        
    """
    # create a list of paths for the json files based on competitions provided
    league_list = []
    for comp in competitions:
        path = filepath + comp
        league_list.extend(glob.glob(path + "/*.json"))

    # initiate empty match dictionary
    match_dict = defaultdict(dict)

    # for each league read corresponding json files
    for league in league_list:
        # create a dataframe for each json file
        df_matches = pd.read_json(league)
        for i in range(len(df_matches)):
            # check if provided team is home or away and extract necessary metadata
            if df_matches.iloc[i, 5]["home_team_name"] == team:
                match_id = str(df_matches.iloc[i, 0])
                match_dict[match_id]["play_loc"] = "home"
                match_dict[match_id]["season"] = df_matches.iloc[i, 4]["season_name"]
                match_dict[match_id]["opposition"] = df_matches.iloc[i, 6][
                    "away_team_name"
                ]

            elif df_matches.iloc[i, 6]["away_team_name"] == team:
                match_id = str(df_matches.iloc[i, 0])
                match_dict[match_id]["play_loc"] = "away"
                match_dict[match_id]["season"] = df_matches.iloc[i, 4]["season_name"]
                match_dict[match_id]["opposition"] = df_matches.iloc[i, 5][
                    "home_team_name"
                ]
    # return final dictionary
    return match_dict
