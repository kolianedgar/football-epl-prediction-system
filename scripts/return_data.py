from utils import (
    slugify
)

import requests
import time

def return_entries(
    header,
    api_urls_matchweek = None,
    api_urls_momentum = None,
    api_urls_stats = None,
    match_ids_raw = [],
    home_away_dict_match_id = {},
    mode = "matchweek"
):

    if mode not in ['matchweek', 'momentum', 'stats']:
        raise ValueError(f"Mode {mode} is invalid")
    
    if mode == "matchweek" and api_urls_matchweek is None:
        raise ValueError("api_urls_matchweek is invalid")

    elif mode == "matchweek" and api_urls_matchweek is not None:
        session = requests.Session()
        session.headers.update(header)

        for api_url in api_urls_matchweek:
            response = session.get(
                api_url,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            for match in data['data']:
                home_away_dict = {}

                match_id = match['matchId']
                home = slugify(match["homeTeam"]["name"])
                away = slugify(match["awayTeam"]["name"])
            
                home_away_dict[home] = away

                home_away_dict_match_id[match_id] = home_away_dict
                match_ids_raw.append(match_id)
        
        return {
            'home_away_dict_match_id': home_away_dict_match_id,
            'match_ids_raw': match_ids_raw
        }

    if mode == "stats" and api_urls_stats is None:
        raise ValueError("api_urls_stats is invalid")

    elif mode == "stats" and api_urls_stats is not None:

        match_stats_entries = {}
        session = requests.Session()
        
        session.headers.update(header)

        for match_id, api_url in zip(match_ids_raw, api_urls_stats):
            try:
                response = session.get(
                    api_url,
                    timeout=30
                )

                if response.status_code == 429:
                    print(f"Rate limited for match {match_id}.")
                    time.sleep(5)
                    continue

                response.raise_for_status()

                data = response.json()
                match_stats_entries[match_id] = data

                time.sleep(0.2)

            except requests.exceptions.JSONDecodeError:
                print(f"Invalid JSON for match {match_id}")
                print("Status:", response.status_code)
                print("Response:", response.text[:300])

            except requests.exceptions.RequestException as e:
                print(f"Request failed for match {match_id}: {e}")

        return match_stats_entries
    
    elif mode == "momentum" and api_urls_momentum is None:
        raise ValueError("api_urls_momentum is invalid")
    
    elif mode == "momentum" and api_urls_momentum is not None:
        match_momentum_entries = {}
        
        session = requests.Session()
        session.headers.update(header)

        for match_id, api_url in zip(match_ids_raw, api_urls_momentum):
            try:
                response = session.get(
                    api_url,
                    timeout=30
                )

                if response.status_code == 429:
                    print(f"Rate limited for match {match_id}.")
                    time.sleep(5)
                    continue

                response.raise_for_status()

                data = response.json()
                match_momentum_entries[match_id] = data

                time.sleep(0.2)

            except requests.exceptions.JSONDecodeError:
                print(f"Invalid JSON for match {match_id}")
                print("Status:", response.status_code)
                print("Response:", response.text[:300])

            except requests.exceptions.RequestException as e:
                print(f"Request failed for match {match_id}: {e}")

        return match_momentum_entries
    
def return_home_away_teams(
    home_away_dict_match_id = None
):
    if home_away_dict_match_id is None:
        raise ValueError("home_away_dict_match_id is invalid")
    
    else:
        games = list(home_away_dict_match_id.values())

        home_teams_full = []
        away_teams_full = []

        for game in games:
            for home_team, away_team in game.items():
                home_teams_full.append(home_team)
                away_teams_full.append(away_team)

        return {
            'home_teams_full': home_teams_full,
            'away_teams_full': away_teams_full
        }

def return_momentum_info(
    match_momentum_entries = None
):
    if match_momentum_entries is None:
        raise ValueError("match_momentum_entries is invalid")

    dates = []
    match_officials = []
    home_team_ht_goals = []
    away_team_ht_goals = []
    home_team_ft_goals = []
    away_team_ft_goals = []

    for idx, data in match_momentum_entries.items():
        match_info = data.get('matchInfo')
        live_data = data.get('liveData')

        if live_data is None:
        
                if len(data.keys()) == 0:
                    continue
                    
                print(f"Missing liveData for the match {idx}. Available keys:", data.keys())
                continue

        if match_info is None:
            print(f"matchInfo about match with ID {idx} is not available yet")
            continue

        match_officials_entries = live_data['matchDetailsExtra']['matchOfficial'][0]
        
        match_officials.append(match_officials_entries['firstName'] + ' ' + match_officials_entries['lastName'])
    
        if "ht" not in live_data["matchDetails"]["scores"].keys():
            home_team_ht_goals.append(live_data["matchDetails"]["scores"]["total"]['home'])
            away_team_ht_goals.append(live_data["matchDetails"]["scores"]["total"]['away'])
    
            print(f"Half-time results for game with ID {idx} are not yet available.")
            print("Using the information that is available.")
            continue
            
        home_team_ht_goals.append(live_data["matchDetails"]["scores"]["ht"]['home'])
        away_team_ht_goals.append(live_data["matchDetails"]["scores"]["ht"]['away'])
    
        home_team_ft_goals.append(live_data["matchDetails"]["scores"]["ft"]['home'])
        away_team_ft_goals.append(live_data["matchDetails"]["scores"]["ft"]['away'])

        dates.append(match_info['localDate'])
        
    return {
        'dates': dates,
        'match_officials': match_officials,
        'home_team_ht_goals': home_team_ht_goals,
        'away_team_ht_goals': away_team_ht_goals,
        'home_team_ft_goals': home_team_ft_goals,
        'away_team_ft_goals': away_team_ft_goals
    }

def return_stats_info(
    match_stats_entries = None,
):
    if match_stats_entries is None:
        raise ValueError("match_stats_entries is invalid")

    home_team_red_cards = []
    home_team_yellow_cards = []
    home_total_shots = []
    home_shots_on_target = []
    home_fouls = []
    home_corners = []

    away_team_red_cards = []
    away_team_yellow_cards = []
    away_total_shots = []
    away_shots_on_target = []
    away_fouls = []
    away_corners = []

    for match_id, data in match_stats_entries.items():
        
        if len(data) == 0:
            continue

        if 'cornerTaken' not in data[1]['stats'].keys():
            home_corners.append(0)
        else:
            home_corners.append(data[1]['stats']['cornerTaken'])

        if 'cornerTaken' not in data[0]['stats'].keys():
            away_corners.append(0)

        else:
            away_corners.append(data[0]['stats']['cornerTaken'])

        if 'ontargetScoringAtt' not in data[1]['stats'].keys():
            home_shots_on_target.append(0)

        else:
            home_shots_on_target.append(data[1]['stats']['ontargetScoringAtt'])

        if 'ontargetScoringAtt' not in data[0]['stats'].keys():
            away_shots_on_target.append(0)

        else:
            away_shots_on_target.append(data[0]['stats']['ontargetScoringAtt'])

        home_team_red_cards.append(data[1]['stats']['totalRedCard'])
        home_team_yellow_cards.append(data[1]['stats']['totalYelCard'])
        home_total_shots.append(data[1]['stats']['totalScoringAtt'])
        home_fouls.append(data[1]['stats']['fkFoulLost'])
        
        away_team_red_cards.append(data[0]['stats']['totalRedCard'])
        away_team_yellow_cards.append(data[0]['stats']['totalYelCard'])
        away_total_shots.append(data[0]['stats']['totalScoringAtt'])
        away_fouls.append(data[0]['stats']['fkFoulLost'])

    return {
        'home_team_red_cards': home_team_red_cards,
        'home_team_yellow_cards': home_team_yellow_cards,
        'home_total_shots': home_total_shots,
        'home_shots_on_target': home_shots_on_target,
        'home_fouls': home_fouls,
        'home_corners': home_corners,  
        'away_team_red_cards': away_team_red_cards,
        'away_team_yellow_cards': away_team_yellow_cards,
        'away_total_shots': away_total_shots,
        'away_shots_on_target': away_shots_on_target,
        'away_fouls': away_fouls,
        'away_corners': away_corners,
    }