from utils import (
    load_data,
    remove_invalid_rows,
    drop_features_until_certain_one,
    parse_date,
    check_missing_values,
    remove_columns,
    report_clean_dataset
)

import os

path = os.getcwd() + "\\data"


df = load_data(path)

df = remove_invalid_rows(df, "Div")
df = remove_columns(df, ["HxG", "AxG", "Time", "HTR"])
df = drop_features_until_certain_one(df, "B365H")
df = parse_date(df, date_column_name="Date", format='mixed', day_first=True)

print(f"Number of missing HomeTeam values: {check_missing_values(df, 'HomeTeam')}")
print(f"Number of missing AwayTeam values: {check_missing_values(df, 'AwayTeam')}")
print(f"Number of missing FTHG values: {check_missing_values(df, 'FTHG')}")
print(f"Number of missing FTAG values: {check_missing_values(df, 'FTAG')}")


print('='*60)

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