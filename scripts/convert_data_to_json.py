from scripts import return_entries
from utils import create_api_urls, slugify
import json

from utils.client_api import APIClient

def convert_home_away_id_to_json(
    url_base = None,
    path = None
):
    if url_base is None:
        raise ValueError("url_base is invalid")

    if path is None:
        raise ValueError("path is invalid")

    client = APIClient()

    try:

        api_urls_matchweek = create_api_urls(
            url_base,
            mode = "matchweek"
        )

        results_matchweek = return_entries(
            client = client,
            api_urls_matchweek = api_urls_matchweek,
            mode = "matchweek"
        )
        
        with open(path, 'w', encoding="utf-8") as fp:
            json.dump(
                results_matchweek["home_away_dict_match_id"],
                fp,
                indent=4
            )
    finally:
        client.close()

def convert_raw_ids_to_json(
    url_base = None,
    path = None
):

    if url_base is None:
        raise ValueError("url_base is invalid")

    if path is None:
        raise ValueError("path is invalid")

    client = APIClient()

    try:
    
        api_urls_matchweek = create_api_urls(
            url_base,
            mode = "matchweek"
        )

        results_matchweek = return_entries(
            client = client,
            api_urls_matchweek = api_urls_matchweek,
            mode = "matchweek"
        )

        with open(path, 'w', encoding="utf-8") as fp:
            json.dump(
                results_matchweek["match_ids_raw"],
                fp,
                indent=4
            )

    finally:
        client.close()

def convert_momentum_to_json(
    url_base = None,
    match_ids = [],
    path = None
):

    if url_base is None:
        raise ValueError("url_base is invalid")

    if path is None:
        raise ValueError("path is invalid")

    client = APIClient()

    try:

        api_urls_momentum = create_api_urls(
            url_base,
            match_ids = match_ids,
            mode = "momentum"
        )

        momentum_entries = return_entries(
            client = client,
            api_urls_momentum = api_urls_momentum,
            mode = "momentum",
            match_ids_raw = match_ids
        )

        with open(path, 'w', encoding="utf-8") as fp:
            json.dump(
                momentum_entries,
                fp,
                indent=4
            )

    finally:
        client.close()

def convert_stats_to_json(
    url_base = None,
    match_ids = [],
    path = None,
):
    if url_base is None:
        raise ValueError("url_base is invalid")

    if path is None:
        raise ValueError("path is invalid")

    client = APIClient()

    try:

        api_urls_stats = create_api_urls(
            url_base,
            match_ids = match_ids,
            mode = "stats"
        )

        stats_entries = return_entries(
            client = client,
            api_urls_stats = api_urls_stats,
            mode = "stats",
            match_ids_raw=match_ids
        )

        with open(path, 'w', encoding="utf-8") as fp:
            json.dump(
                stats_entries,
                fp,
                indent=4
            )

    finally:
        client.close()