import glob
import pandas as pd
import os
import json

def load_data(path):
    files = glob.glob(path + "\\*.csv")

    all_dataframes = []

    for file in files:
        try:
            temp_dataframe = pd.read_csv(file, encoding = 'utf-8')
            all_dataframes.append(temp_dataframe)

        except Exception as e:
            print(f"Could not read file {file} due to: {e}")

    if all_dataframes:
        df = pd.concat(all_dataframes, ignore_index = True)
        print('=' * 60)
        print(f"Success! Combined DataFrame shape: {df.shape}")
        print(f"Number of files loaded: {len(files)}")
        print(f"Number of rows: {len(df.index)}")
        print(f"Number of columns: {len(df.columns)}")
        return df

    else:
        print("No files were successfully read.")
        return None

def load_all_data(
    path
):
    if not os.path.exists(path):
        raise ValueError(f"{path} does not exist")

    df = pd.read_csv(
        path,
        encoding = 'utf-8'
    )

    return df

def load_json(
    path
):

    if not os.path.exists(path):
        raise ValueError(f"{path} does not exist")

    with open(path, "r", encoding='utf-8') as file:
        return json.load(file)