from scripts import return_entries
from utils import create_api_urls, slugify
import json
import requests

def convert_data_to_json(
    header = None,
    url_base = None,
    match_ids = [],
    mode = "matchweek"
):

    if header is None:
        raise ValueError("Requests header is invalid")
    
    if mode not in ['matchweek', 'momentum', 'stats']:
        raise ValueError(f"Mode {mode} is invalid")

    if mode == "matchweek":
        home_away_dict_match_id = {}
        match_ids_raw = []

        api_urls_matchweek = create_api_urls(
            url_base,
            mode = "matchweek"
        )

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
        
        with open('home_away_id.json', 'w') as fp:
            json.dump(home_away_dict_match_id, fp)

        with open('ids_raw.json', 'w') as fp:
            json.dump(match_ids_raw, fp)
            
        
    elif mode == "momentum":
        api_urls_momentum = create_api_urls(
            url_base,
            match_ids = match_ids,
            mode = mode
        )

        momentum_entries = return_entries(
            header = header,
            api_urls_momentum = api_urls_momentum,
            mode = mode
        )

        with open('momentum.json', 'w') as fp:
            json.dump(momentum_entries, fp)

    elif mode == "stats":
        api_urls_stats = create_api_urls(
            url_base,
            match_ids = match_ids,
            mode = mode
        )

        stats_entries = return_entries(
            header = header,
            api_urls_stats = api_urls_stats,
            mode = mode
        )

        with open('stats.json', 'w') as fp:
            json.dump(stats_entries, fp)
    