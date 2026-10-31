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
    determine_result_of_ht,
    determine_result_of_ft
)

from scripts import (
    return_home_away_teams,
    return_momentum_info,
    return_stats_info,
    convert_data_to_json
)

import os
import json
import pandas as pd
import numpy as np

path = os.getcwd() + "\\data"


df = load_data(path)

df = remove_invalid_rows(df, "Referee")
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

# print(df_elo.head())

print('=' * 60)

api_urls_momentum = []
api_urls_stats = []

number_of_matchweeks = 38

url_base_matchweek = "https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v2/matches?competition=8&season=2026&matchweek=1&_limit=20"
url_base_momentum = "https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v1/matches/2645272/momentum"
url_base_stats = "https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v3/matches/2645272/stats"

# convert_data_to_json(
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

print('=' * 60)

# convert_data_to_json(
#     url_base = url_base_momentum,
#     match_ids = match_ids_raw,
#     mode = "momentum"
# )

# convert_data_to_json(
#     url_base = url_base_stats,
#     match_ids = match_ids_raw,
#     mode = "stats"
# )

with open('momentum.json') as file:
    momentum_entries = json.load(file)

with open('stats.json') as file:
    stats_entries = json.load(file)

results_momentum = return_momentum_info(
    match_momentum_entries = momentum_entries
)

dates = results_momentum['dates']
match_officials = results_momentum['match_officials']
home_team_ht_goals = results_momentum['home_team_ht_goals']
away_team_ht_goals = results_momentum['away_team_ht_goals']
home_team_ft_goals = results_momentum['home_team_ft_goals']
away_team_ft_goals = results_momentum['away_team_ft_goals']

results_stats = return_stats_info(
    match_stats_entries = stats_entries
)

home_team_red_cards = results_stats['home_team_red_cards']
home_team_yellow_cards = results_stats['home_team_yellow_cards']
home_total_shots = results_stats['home_total_shots']
home_shots_on_target = results_stats['home_shots_on_target']
home_fouls = results_stats['home_fouls']
home_corners = results_stats['home_corners']

away_team_red_cards = results_stats['away_team_red_cards']
away_team_yellow_cards = results_stats['away_team_yellow_cards']
away_total_shots = results_stats['away_total_shots']
away_shots_on_target = results_stats['away_shots_on_target']
away_fouls = results_stats['away_fouls']
away_corners = results_stats['away_corners']

df_new_data = pd.DataFrame(
    columns=[
        'HomeTeam',
        'AwayTeam',
        'HTHG',
        'HTAG',
        'HTR',
        'Referee',
        'HS',
        'AS',
        'HST',
        'AST',
        'HF',
        'AF',
        'HC',
        'AC',
        'HY',
        'AY',
        'HR',
        'AR',
        'HomeElo',
        'AwayElo',
        'EloDifference'
    ]
)

df_new_data["HomeTeam"] = home_teams
df_new_data["AwayTeam"] = away_teams

df_new_data["HomeTeam"] = df_new_data["HomeTeam"].replace(to_replace=r'-', value=' ', regex=True)
df_new_data["AwayTeam"] = df_new_data["AwayTeam"].replace(to_replace=r'-', value=' ', regex=True)

df_new_data["HomeTeam"] = df_new_data["HomeTeam"].str.title()
df_new_data["AwayTeam"] = df_new_data["AwayTeam"].str.title()

df_new_data["HTHG"] = pd.Series(home_team_ht_goals)
df_new_data["HTAG"] = pd.Series(away_team_ht_goals)
df_new_data["Referee"] = pd.Series(match_officials)
df_new_data["HS"] = pd.Series(home_total_shots)
df_new_data["AS"] = pd.Series(away_total_shots)
df_new_data["HST"] = pd.Series(home_shots_on_target)
df_new_data["AST"] = pd.Series(away_shots_on_target)
df_new_data["HF"] = pd.Series(home_fouls)
df_new_data["AF"] = pd.Series(away_fouls)
df_new_data["HC"] = pd.Series(home_corners)
df_new_data["AC"] = pd.Series(away_corners)
df_new_data["HY"] = pd.Series(home_team_yellow_cards)
df_new_data["AY"] = pd.Series(away_team_yellow_cards)
df_new_data["HR"] = pd.Series(home_team_red_cards)
df_new_data["AR"] = pd.Series(away_team_red_cards)

df_new_data["FTHG"] = pd.Series(home_team_ft_goals)
df_new_data["FTAG"] = pd.Series(away_team_ft_goals)


df_new_data['HTR'] = df_new_data.apply(determine_result_of_ht, axis=1)
df_new_data['FTR'] = df_new_data.apply(determine_result_of_ft, axis=1)

df_new_data = df_new_data[df_new_data['Referee'].notna()]

df_new_data.loc[:,'Date'] = dates

dates_col = df_new_data.pop('Date')
df_new_data.insert(0, 'Date', dates_col)
df_new_data['Date'] = df_new_data['Date'].str.strip("Z")


df_new_data = parse_date(
    df = df_new_data,
    date_column_name='Date',
    format = 'mixed'
)

df_new_data = sort_chronologically(df_new_data, "Date")

df_new_full_w_duplicates = pd.concat([df, df_new_data])
df_new_full = df_new_full_w_duplicates.drop_duplicates()

print(df_new_data["Date"].max())

df_new_elo = add_elo_columns_to_dataframe(
    df_new_full,
    home_team_col="HomeTeam",
    away_team_col="AwayTeam",
    fthg="FTHG",
    ftag="FTAG",
    ftr="FTR"
)

df_new_elo = df_new_elo.drop(columns=["Div"])

X_new_elo, y_new_elo = split_data_features_targets(
    df_new_elo,
    date_column="Date",
    columns_to_drop=["FTHG", "FTAG", "Date"],
    target_column="FTR"
)