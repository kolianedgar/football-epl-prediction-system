import pandas as pd

def report_clean_dataset(
    df,
    date_column = None,
    division_column = None,
    target_column = None,
    fthg = None,
    ftag = None,
    home_team_col = None,
    away_team_col = None
):

    if df is None:
        raise ValueError(f"The DataFrame {df} is invalid")

    columns_to_check = [
        date_column,
        division_column,
        target_column,
        fthg,
        ftag,
        home_team_col,
        away_team_col
    ]

    for col in columns_to_check:
        if col is not None and col not in df.columns:
            raise ValueError(f"Column {col} not found in the dataframe!")

        if col is None:
            raise ValueError(f"Column {col} is invalid!")

    earliest_date = df[date_column].min()
    latest_date = df[date_column].max()

    unique_team_count = len(df[home_team_col].unique())

    unique_divisions_count = len(df[division_column].unique())

    missing_values_count = df.isnull().sum().sum()

    unique_target_values = df[target_column].unique().tolist()


    # Invalid home goals
    invalid_home = df[fthg] < 0

    # Invalid away goals
    invalid_away = df[ftag] < 0

    home_only_invalid = invalid_home & ~invalid_away
    away_only_invalid = invalid_away & ~invalid_home
    both_invalid = invalid_home & invalid_away

    home_team_invalid_count = home_only_invalid.sum()
    away_team_invalid_count = away_only_invalid.sum()
    both_invalid_count = both_invalid.sum()

    identical_home_and_away = (df[home_team_col] == df[away_team_col]).sum()

    return {
        "Number of matches": len(df.index),
        "Earliest date": earliest_date,
        "Latest date": latest_date,
        "Number of unique teams": unique_team_count,
        "Number of unique divisions": unique_divisions_count,
        "Number of missing values": missing_values_count,
        "Unique target values": unique_target_values,
        "Only_home goals invalid": home_team_invalid_count,
        "Only_away_goals_invalid": away_team_invalid_count,
        "Both_invalid": both_invalid_count,
        "Identical home and away": identical_home_and_away
    }