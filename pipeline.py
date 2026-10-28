import time

from utils import (
    load_data,
    remove_invalid_rows,
    keep_features_until_certain_one,
    parse_date,
    check_missing_values,
    remove_columns,
    report_clean_dataset,
    sort_chronologically,
    add_elo_columns_to_dataframe,
    split_data_features_targets,
    split_df_train_test,
    slugify,
    create_api_urls,
    determine_result_of_ht
)

from scripts import (
    return_entries,
    return_home_away_teams,
    convert_data_to_json
)

import os
import json

path = os.getcwd() + "\\data"


df = load_data(path)

df = remove_invalid_rows(df, "Div")
df = remove_columns(df, ["HxG", "AxG", "Time"])
df = keep_features_until_certain_one(df, "B365H")
df = parse_date(df, date_column_name="Date", format='mixed', day_first=True)

print('=' * 60)
print(f"Number of missing HomeTeam values: {check_missing_values(df, 'HomeTeam')}")
print(f"Number of missing AwayTeam values: {check_missing_values(df, 'AwayTeam')}")
print(f"Number of missing FTHG values: {check_missing_values(df, 'FTHG')}")
print(f"Number of missing FTAG values: {check_missing_values(df, 'FTAG')}")


print('=' * 60)

report = report_clean_dataset(
    df, 
    date_column = "Date",
    division_column = "Div",
    target_column = "FTR",
    fthg = "FTHG",
    ftag = "FTAG",
    home_team_col = "HomeTeam",
    away_team_col = "AwayTeam"
)

for key, value in report.items():
    print(f"{key}: {value}")

df = sort_chronologically(df, "Date")

df_elo = add_elo_columns_to_dataframe(
    df,
    home_team_col="HomeTeam",
    away_team_col="AwayTeam",
    fthg="FTHG",
    ftag="FTAG",
    ftr="FTR"
)

X, y = split_data_features_targets(
    df_elo,
    date_column="Date",
    columns_to_drop=["Div", "FTHG", "FTAG", "Date"],
    target_column="FTR"
)

X_train, X_test, y_train, y_test = split_df_train_test(
    X,
    y,
    split_proportion=0.8
)

print('='*60)
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)
print('='*60)
print(X_train.columns.tolist())

print('='*60)

header = {
    "User-Agent": "Mozilla/5.0"
}

api_urls_momentum = []
api_urls_stats = []

home_away_dict_match_id = {}
match_ids_raw = []

number_of_matchweeks = 38

url_base_matchweek = "https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v2/matches?competition=8&season=2026&matchweek=1&_limit=20"
url_base_momentum = "https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v1/matches/2645272/momentum"
url_base_stats = "https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v3/matches/2645272/stats"

# convert_data_to_json(
#     header = header,
#     url_base=url_base_matchweek,
#     mode = "matchweek"
# )

with open('home_away_id.json') as file:
    home_away_dict_match_id = json.load(file)

with open('ids_raw.json') as file:
    match_ids_raw = json.load(file)

results_home_away = return_home_away_teams(
    home_away_dict_match_id=home_away_dict_match_id
)

home_teams = results_home_away['home_teams_full']
away_teams = results_home_away['away_teams_full']

print(f"First 5 home teams: {home_teams[:5]}")
print(f"First 5 away teams: {away_teams[:5]}")

# convert_data_to_json(
#     header = header,
#     url_base = url_base_momentum,
#     match_ids = match_ids_raw,
#     mode = "momentum"
# )

# convert_data_to_json(
#     header = header,
#     url_base = url_base_stats,
#     match_ids = match_ids_raw,
#     mode = "stats"
# )

with open('momentum.json') as file:
    momentum_entries = json.load(file)

with open('stats.json') as file:
    stats_entries = json.load(file)