import os
from datetime import date

from scripts import (
    return_home_away_teams,
    return_momentum_info,
    return_stats_info,

    convert_home_away_id_to_json,
    convert_raw_ids_to_json,
    convert_momentum_to_json,
    convert_stats_to_json
)

from utils import (
    load_data,
    load_all_data,
    load_json,
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
    determine_result_of_ft,
    backup_data,
    create_backup_folder
)

path_matches = os.getcwd() + "\\data\\primary\\all_matches.csv"
path_home_away_match_id = os.getcwd() + "\\data\\primary\\home_away_id.json"
path_ids = os.getcwd() + "\\data\\primary\\ids_raw.json"
path_momentum = os.getcwd() + "\\data\\primary\\momentum.json"
path_stats = os.getcwd() + "\\data\\primary\\stats.json"

path_primary_files = os.getcwd() + "\\data\\primary\\"
path_backup_dst = os.getcwd() + "\\data\\backup\\"

matches = load_all_data(
    path = path_matches
)

print('*' * 60)
print(matches.head())
print('*' * 60)

home_away_match_id = load_json(
    path = path_home_away_match_id
)

ids_raw = load_json(
    path = path_ids
)

momentum = load_json(
    path = path_momentum
)

stats = load_json(
    path = path_stats
)

backup_folder_path = create_backup_folder(
    dst_dir = path_backup_dst
)

for file_name in os.listdir(path_primary_files):
    backup_data(
        src_dir = path_primary_files,
        src_file_name = file_name,
        dst_dir = backup_folder_path
    )