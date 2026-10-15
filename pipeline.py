from utils import (
    load_data,
    remove_invalid_rows,
    drop_features_until_certain_one,
    parse_date,
    check_missing_values,
    remove_columns,
    report_clean_dataset,
    sort_chronologically,
    add_elo_columns_to_dataframe,
    split_data_features_targets,
    split_df_train_test
)

import os

path = os.getcwd() + "\\data"


df = load_data(path)

df = remove_invalid_rows(df, "Div")
df = remove_columns(df, ["HxG", "AxG", "Time", "HTR"])
df = drop_features_until_certain_one(df, "B365H")
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

# print('='*60)
# print("Last rows of the new dataframe with ELO")
# print('='*60)
# print(df_elo_test.tail())

X, y = split_data_features_targets(
    df_elo,
    date_column="Date",
    columns_to_drop=["FTHG", "FTAG", "Date"],
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

print(X.columns.tolist())