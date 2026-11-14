import pandas as pd

def remove_invalid_rows(
    df,
    column_of_reference
):
    if column_of_reference not in df.columns:
        raise ValueError(f"Column {column_of_reference} not found")

    return df[df[column_of_reference].notna()]

def keep_features_until_certain_one(
    df,
    column_name
):
    if column_name not in df.columns:
        raise ValueError(f"Column {column_name} not found")

    return df.iloc[:, :df.columns.tolist().index(column_name)]

def remove_columns(
    df,
    columns
):
    columns_to_drop = []

    for column_ref in columns:
        if column_ref not in df.columns:
            raise ValueError(f"Column {column_ref} not found")

        columns_to_drop.append(column_ref)
        
    return df.drop(columns = columns_to_drop)

def parse_date(
    df,
    date_column_name,
    format,
    day_first = False
):
    if date_column_name not in df.columns:
        raise ValueError(f"Column {date_column_name} not found")
    
    df[date_column_name] = pd.to_datetime(df[date_column_name].astype(str), format=format, dayfirst=day_first)
    return df[date_column_name]

def parse_time(
    df,
    time_column_name
):
    if time_column_name not in df.columns:
        raise ValueError(f"Column {time_column_name} not found")

    df[time_column_name] = pd.to_datetime(df[time_column_name].astype(str), format='%H:%M:%S').dt.tz_localize("GMT")
    df[time_column_name] = df[time_column_name].dt.time
    
    return df[time_column_name]

def create_datetime(
    df,
    date_column_name,
    time_column_name,
    datetime_column_name
):
    if date_column_name not in df.columns:
        raise ValueError(f"Column {date_column_name} not found")
    
    if time_column_name not in df.columns:
        raise ValueError(f"Column {time_column_name} not found")

    df[datetime_column_name] = pd.to_datetime(df[date_column_name].astype(str) + ' ' + df[time_column_name].astype(str))
    
    return df[datetime_column_name]

def check_missing_values(
    df,
    column
):
    if column not in df.columns:
        raise ValueError(f"Column {column} not found")

    return df[column].isna().sum()

def sort_chronologically(
    df,
    date_column = None,
    mode = "date",
    datetime_column = None
):

    if mode.lower() not in ['date', 'datetime']:
        raise ValueError(f"Mode {mode} is invalid")

    if mode.lower() == 'date':
        if date_column not in df.columns:
            raise ValueError(f"Column {date_column} not found")

        if date_column is not None:
            df.sort_values(by=date_column, inplace=True)
            df.reset_index(drop=True, inplace=True)
            return df
        
        elif date_column is None:
            raise ValueError("date_column is invalid")

    if mode.lower() == 'datetime':
        if datetime_column not in df.columns:
            raise ValueError(f"Column {datetime_column} not found")

        if datetime_column is not None:
            df.sort_values(by=datetime_column, ascending = True)
            df.drop(columns=datetime_column).reset_index(drop=True)

            return df

        elif datetime_column is None:
            raise ValueError("datetime_column is invalid")