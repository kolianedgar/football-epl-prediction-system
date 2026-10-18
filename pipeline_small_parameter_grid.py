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
    split_df_train_test
)

from sklearn.model_selection import GridSearchCV
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report

import os

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

model = CatBoostClassifier(
    logging_level = 'Silent',
    allow_writing_files = False
)

parameter_grid = {
    "iterations": [100, 200],
    "learning_rate": [0.01, 0.1],
    "depth": [4, 6, 8],
    "l2_leaf_reg": [1, 3, 5],
    "border_count": [32, 64, 128],
}

grid_search = GridSearchCV(
    estimator = model,
    param_grid = parameter_grid,
    cv = 3,
    verbose = 2,
    n_jobs = -1
)

curr_time = time.time()
grid_search.fit(X_train, y_train, cat_features = ["HomeTeam", "AwayTeam", "HTR", "Referee"])
end = time.time()

print(f"Time taken for hyperparameter tuning: {end - curr_time}")

final_model = grid_search.best_estimator_

y_train_pred = final_model.predict(X_train)
y_pred = final_model.predict(X_test)

print('=' * 60)
print(f"Best Parameters: {grid_search.best_params_}")
print('=' * 60)

# Best Parameters: {
#   'border_count': 128,
#   'depth': 8,
#   'iterations': 100,
#   'l2_leaf_reg': 5,
#   'learning_rate': 0.1
# }

print("Training Classification Report:")
print(classification_report(y_train, y_train_pred))
print('=' * 60)

print("Testing Classification Report:")
print(classification_report(y_test, y_pred))

# Training Classification Report:
#               precision    recall  f1-score   support

#            A       0.73      0.79      0.75      1914
#            D       0.61      0.41      0.49      1566
#            H       0.77      0.86      0.81      2944

#     accuracy                           0.73      6424
#    macro avg       0.70      0.69      0.69      6424
# weighted avg       0.72      0.73      0.72      6424

# ============================================================
# Testing Classification Report:
#               precision    recall  f1-score   support

#            A       0.65      0.70      0.68       505
#            D       0.39      0.30      0.34       391
#            H       0.72      0.77      0.75       710

#     accuracy                           0.64      1606
#    macro avg       0.59      0.59      0.59      1606
# weighted avg       0.62      0.64      0.62      1606
