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
        for api_url in api_urls_matchweek:
            response = requests.get(
                api_url,
                headers=header,
                timeout=20
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
        session = requests.Session()
        session.headers.update(header)
        match_stats_entries = {}

        for match_id, api_url in zip(match_ids_raw, api_urls_stats):
            try:
                response = session.get(api_url, timeout=30)

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
                response = session.get(api_url, timeout=30)

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