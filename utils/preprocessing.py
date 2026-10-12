import pandas as pd

def remove_invalid_rows(df, column_of_reference):
    if column_of_reference not in df.columns:
        raise ValueError(f"Column {column_of_reference} not found")

    return df[df[column_of_reference].notna()]

def drop_features_until_certain_one(df, column_name):
    if column_name not in df.columns:
        raise ValueError(f"Column {column_name} not found")

    return df.iloc[:, :df.columns.tolist().index(column_name)]

def remove_columns(df, columns):
    columns_to_drop = []

    for column_ref in columns:
        if column_ref not in df.columns:
            raise ValueError(f"Column {column_ref} not found")

        columns_to_drop.append(column_ref)
        
    return df.drop(columns = columns_to_drop)

def parse_date(df, date_column_name, format, day_first):
    if date_column_name not in df.columns:
        raise ValueError(f"Column {date_column_name} not found")
    
    df[date_column_name] = pd.to_datetime(df[date_column_name], format=format, dayfirst=day_first)
    return df

def check_missing_values(df, column):
    if column not in df.columns:
        raise ValueError(f"Column {column} not found")

    return df[column].isna().sum()