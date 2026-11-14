from utils import (
    load_data,
    remove_invalid_rows,
    keep_features_until_certain_one,
    parse_date,
    parse_time,
    check_missing_values,
    remove_columns,
    report_clean_dataset,
    sort_chronologically,
    add_elo_columns_to_dataframe,
    determine_result_of_ht,
    determine_result_of_ft,
    load_json,
    create_datetime
)

from scripts import (
    return_home_away_teams,
    return_momentum_info,
    return_stats_info,

    convert_home_away_id_to_json,
    convert_raw_ids_to_json,
    convert_momentum_to_json,
    convert_stats_to_json,
    convert_match_id_datetime_to_json
)

import os
import pandas as pd

# Load Data From CSV Files
path = os.getcwd() + "\\data"

df = load_data(path)
df = remove_invalid_rows(df, "Referee")
df = remove_columns(df, ["HxG", "AxG", "Time"])
df = keep_features_until_certain_one(df, "B365H")
df['Date'] = parse_date(df, date_column_name="Date", format='mixed', day_first=True)

print('=' * 60)

print("Dataset after cleaning:")

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

df = sort_chronologically(
    df,
    date_column="Date",
    mode = "date"
)

api_urls_momentum = []
api_urls_stats = []

number_of_matchweeks = 38

# URLs of APIs providing the information
url_base_matchweek = "https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v2/matches?competition=8&season=2026&matchweek=1&_limit=20"
url_base_momentum = "https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v1/matches/2645272/momentum"
url_base_stats = "https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v3/matches/2645272/stats"

# Establish paths where the primary files should be saved
path_momentum = os.getcwd() + "\\data\\primary\\momentum.json"
path_stats = os.getcwd() + "\\data\\primary\\stats.json"
path_home_away_id = os.getcwd() + "\\data\\primary\\home_away_id.json"
path_ids_raw = os.getcwd() + "\\data\\primary\\ids_raw.json"
path_id_kickoff_time = os.getcwd() + "\\data\\primary\\id_kickoff_time.json"

# Gather data from APIs with a shared session:
    # Home-Away matches, keyed by MatchID
    # Raw MatchIDs
    # Kick-off dates and times, keyed by MatchID
# Save into separate JSON files

# convert_home_away_id_to_json(
#     url_base = url_base_matchweek,
#     path = path_home_away_id
# )

# convert_raw_ids_to_json(
#     url_base = url_base_matchweek,
#     path = path_ids_raw
# )

# convert_match_id_datetime_to_json(
#     url_base = url_base_matchweek,
#     path = path_id_kickoff_time
# )

# Load relevant information from JSON files
home_away_dict_match_id = load_json(path_home_away_id)    
match_ids_raw = load_json(path_ids_raw)
momentum_entries = load_json(path_momentum)
stats_entries = load_json(path_stats)
match_id_kickoff_time = load_json(path_id_kickoff_time)

# Gather data from APIs with a shared session:
    # Momentum entries
    # Stats entries
# Save into separate JSON files
# convert_momentum_to_json(
#     url_base = url_base_momentum,
#     match_ids = match_ids_raw,
#     path = path_momentum
# )

# convert_stats_to_json(
#     url_base = url_base_stats,
#     match_ids = match_ids_raw,
#     path = path_stats
# )

# Get complex Dictionary Structures from JSON files
results_home_away = return_home_away_teams(
    home_away_dict_match_id=home_away_dict_match_id
)
results_momentum = return_momentum_info(
    match_momentum_entries = momentum_entries
)
results_stats = return_stats_info(
    match_stats_entries = stats_entries
)

home_teams = results_home_away['home_teams_full']
away_teams = results_home_away['away_teams_full']
date_times_full = list(match_id_kickoff_time.values())

# Separate Dates and Kick-Off times
dates = []
kickoff_times = []
for datetime in date_times_full:
    dates.append(datetime[:10])
    kickoff_times.append(datetime[11:])

# Create and populate the final tabular dataset with ready-to-use values
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

# Populate home and away teams into the dataset
# Initial format: manchester-city, ...
# Separate words: manchester city, ...
# Make the names label (every word starting from capital letter): Manchester City, ...
df_new_data["HomeTeam"] = pd.Series(home_teams)
df_new_data["AwayTeam"] = pd.Series(away_teams)
df_new_data["HomeTeam"] = df_new_data["HomeTeam"].replace(to_replace=r'-', value=' ', regex=True)
df_new_data["AwayTeam"] = df_new_data["AwayTeam"].replace(to_replace=r'-', value=' ', regex=True)
df_new_data["HomeTeam"] = df_new_data["HomeTeam"].str.title()
df_new_data["AwayTeam"] = df_new_data["AwayTeam"].str.title()

# Populate home-team-related metrics: half-time goals, shots, ...
df_new_data["HTHG"] = pd.Series(results_momentum['home_team_ht_goals'])
df_new_data["HS"] = pd.Series(results_stats['home_total_shots'])
df_new_data["HST"] = pd.Series(results_stats['home_shots_on_target'])
df_new_data["HF"] = pd.Series(results_stats['home_fouls'])
df_new_data["HC"] = pd.Series(results_stats['home_corners'])
df_new_data["HY"] = pd.Series(results_stats['home_team_yellow_cards'])
df_new_data["HR"] = pd.Series(results_stats['home_team_red_cards'])
df_new_data["FTHG"] = pd.Series(results_momentum['home_team_ft_goals'])

# Populate away-team-related metrics: half-time goals, shots, ...
df_new_data["HTAG"] = pd.Series(results_momentum['away_team_ht_goals'])
df_new_data["AS"] = pd.Series(results_stats['away_total_shots'])
df_new_data["AST"] = pd.Series(results_stats['away_shots_on_target'])
df_new_data["AF"] = pd.Series(results_stats['away_fouls'])
df_new_data["AC"] = pd.Series(results_stats['away_corners'])
df_new_data["AY"] = pd.Series(results_stats['away_team_yellow_cards'])
df_new_data["AR"] = pd.Series(results_stats['away_team_red_cards'])
df_new_data["FTAG"] = pd.Series(results_momentum['away_team_ft_goals'])

# Populate referee names into the dataset
df_new_data["Referee"] = pd.Series(results_momentum['match_officials'])

# Calculate Values and Populate HTR and FTR columns
df_new_data['HTR'] = df_new_data.apply(determine_result_of_ht, axis=1)
df_new_data['FTR'] = df_new_data.apply(determine_result_of_ft, axis=1)

# Populate Date-related columns of the dataset
df_new_data['Date'] = dates
df_new_data['Time'] = kickoff_times

# Parse values of Dates and Time columns
df_new_data['Date'] = parse_date(
    df = df_new_data,
    date_column_name='Date',
    format = 'mixed'
)
df_new_data["Time"] = parse_time(
    df = df_new_data,
    time_column_name="Time"
)

# Create and Populate DateTime column
# Format: 'YYYY-MM-DD HH:MM:SS'
df_new_data["DateTime"] = create_datetime(
    df_new_data,
    date_column_name="Date",
    time_column_name="Time",
    datetime_column_name="DateTime"
)

#Sort values by 'DateTime': from newest to oldest
df_new_data = sort_chronologically(
    df = df_new_data,
    mode = 'datetime',
    datetime_column = "DateTime"
)

# Drop the 'Time' column
# Unrelevant for prediction and is not present in old games
df_new_data = df_new_data.drop(columns=['Time'])

# Dataset without Division, Time, DateTime
# Relevant column remaining: Date
df_without_date_time = df_new_data.drop(columns=['DateTime'])
df_new_full = pd.concat([df, df_without_date_time])
df_new_full = df_new_full.drop(columns=['Div'])
df_new_full = df_new_full.drop_duplicates()

# Dataset without Div, Date, Time
# Relevant column remaining: DateTime
df_new_full_with_date_time = pd.concat([df, df_new_data]).drop_duplicates()
df_new_full_with_date_time = df_new_full_with_date_time.drop(columns=['Date', 'Div'])
df_new_full_with_date_time = df_new_full_with_date_time.drop_duplicates()

# Add ELO-related features to the dataset
# Features added: HomeElo, AwayElo, EloDifference
df_new_elo = add_elo_columns_to_dataframe(
    df_new_full,
    home_team_col="HomeTeam",
    away_team_col="AwayTeam",
    fthg="FTHG",
    ftag="FTAG",
    ftr="FTR"
)
df_new_elo_date_time = add_elo_columns_to_dataframe(
    df_new_full_with_date_time,
    home_team_col="HomeTeam",
    away_team_col="AwayTeam",
    fthg="FTHG",
    ftag="FTAG",
    ftr="FTR"
)

# Bring DateTime column, making it the first
datetime_col = df_new_elo_date_time.pop('DateTime')
df_new_elo_date_time.insert(0, "DateTime", datetime_col)

# Separate matches that have not happened yet
new_matches = df_new_elo_date_time[df_new_elo_date_time['FTR'].isna()]

# Separate matches that have already happened
old_matches = df_new_elo[df_new_elo['FTR'].notna()]

# Save datasets into separate CSV files
old_matches.to_csv(os.getcwd() + "\\data\\primary\\all_matches.csv", index=False)
new_matches.to_csv(os.getcwd() + "\\data\\primary\\new_matches.csv", index=False)