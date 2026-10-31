from scripts import return_entries
from utils import create_api_urls, slugify
import json
import requests

def convert_data_to_json(
    url_base = None,
    match_ids = [],
    mode = "matchweek"
):

    if mode not in ['matchweek', 'momentum', 'stats']:
        raise ValueError(f"Mode {mode} is invalid")

    if mode == "matchweek":

        header = {
            "User-Agent": "Mozilla/5.0"
        }

        api_urls_matchweek = create_api_urls(
            url_base,
            mode = "matchweek"
        )

        results_matchweek = return_entries(
            header = header,
            api_urls_matchweek = api_urls_matchweek,
            mode = "matchweek"
        )
        
        with open('home_away_id.json', 'w', encoding="utf-8") as fp:
            json.dump(results_matchweek["home_away_dict_match_id"], fp, indent=4)

        with open('ids_raw.json', 'w', encoding="utf-8") as fp:
            json.dump(results_matchweek["match_ids_raw"], fp, indent=4)
            
        
    elif mode == "momentum":
        header = {
            "User-Agent": "Mozilla/5.0"
        }

        api_urls_momentum = create_api_urls(
            url_base,
            match_ids = match_ids,
            mode = "momentum"
        )

        momentum_entries = return_entries(
            header = header,
            api_urls_momentum = api_urls_momentum,
            mode = "momentum"
        )

        with open('momentum.json', 'w', encoding="utf-8") as fp:
            json.dump(momentum_entries, fp, indent=4)

    elif mode == "stats":
        header = {
            "User-Agent": "Mozilla/5.0"
        }

        api_urls_stats = create_api_urls(
            url_base,
            match_ids = match_ids,
            mode = "stats"
        )

        stats_entries = return_entries(
            header = header,
            api_urls_stats = api_urls_stats,
            mode = "stats"
        )

        with open('stats.json', 'w', encoding="utf-8") as fp:
            json.dump(stats_entries, fp, indent=4)
    