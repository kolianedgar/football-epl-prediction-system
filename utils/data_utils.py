import re
import numpy as np
import pandas as pd

def slugify(name):
    return re.sub(r"-+", "-", re.sub(
        r"[^a-z0-9]+", "-", name.lower()
    )).strip("-")

def determine_result_of_ht(row):
    if row['HTHG'] > row['HTAG']:
        return 'H'
    elif row['HTHG'] < row['HTAG']:
        return 'A'
    elif row['HTHG'] == np.nan and row['HTAG'] == np.nan:
        return pd.NA
    elif row['HTHG'] == row['HTAG']:
        return 'D'

def _change_matchweek(url, matchweek):
    pattern = r"(matchweek=)\d+"
    return re.sub(pattern, rf"\g<1>{matchweek}", url)

def _change_match_id(url, match_id):
    pattern = r"(/matches/)\d+"
    return re.sub(pattern, rf"\g<1>{match_id}", url)

def create_api_urls(
    url_base = None,
    number_of_matchweeks = 38,
    match_ids = None,
    mode = "matchweek"
):

    api_urls_matchweek = []
    api_urls_momentum = []
    api_urls_stats = []

    if url_base is None:
        raise ValueError("URL of the API is None")

    if mode not in ['matchweek', 'momentum', 'stats']:
        raise ValueError(f"Mode {mode} is invalid")

    if mode == "matchweek":
        for i in range(1, number_of_matchweeks+1):
            api_urls_matchweek.append(_change_matchweek(url_base, i))
            
        return api_urls_matchweek
    
    elif mode == "momentum" and match_ids is None:
        raise ValueError(f"match_ids is None. Mode: {mode}")

    elif mode == "momentum" and match_ids is not None:
        for idx in match_ids:
            api_urls_momentum.append(_change_match_id(url_base, idx))

        return api_urls_momentum

    elif mode == "stats" and match_ids is None:
        raise ValueError(f"match_ids is None. Mode: {mode}")

    elif mode == "stats" and match_ids is not None:
        for idx in match_ids:
            api_urls_stats.append(_change_match_id(url_base, idx))

        return api_urls_stats