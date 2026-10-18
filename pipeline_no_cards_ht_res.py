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

from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
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
    columns_to_drop=[
        "Div",
        "FTHG",
        "FTAG",
        "Date",
        "HTR",
        "HTHG",
        "HTAG",
        "HY",
        "HR",
        "AY",
        "AR"
    ],
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

tscv = TimeSeriesSplit (
    n_splits = 5
)

model = CatBoostClassifier(
    eval_metric="TotalF1",
    random_seed=42,
    verbose=0,
    allow_writing_files=False,
    thread_count=-1,
    loss_function="MultiClass"
)

parameter_grid = {
    "depth": [5, 6, 7],
    "iterations": [300, 500],
    "learning_rate": [0.03, 0.05, 0.1],
    "l2_leaf_reg": [5, 7, 9],
    "border_count": [64, 128]
}

grid_search = GridSearchCV(
    estimator = model,
    param_grid = parameter_grid,
    cv = 3,
    verbose = 2,
    n_jobs = -1,
    refit = True,
    scoring = "f1_macro"
)



curr_time = time.time()
grid_search.fit(X_train, y_train, cat_features = ["HomeTeam", "AwayTeam", "Referee"])
end = time.time()

print(f"Time taken for hyperparameter tuning: {end - curr_time}")

final_model = grid_search.best_estimator_

y_train_pred = final_model.predict(X_train)
y_pred = final_model.predict(X_test)

print('=' * 60)
print(f"Best Parameters: {grid_search.best_params_}")

# Best Parameters: {
#   'border_count': 64,
#   'depth': 5,
#   'iterations': 500,
#   'l2_leaf_reg': 9,
#   'learning_rate': 0.1
# }

print(f"Best CV macro-f1: {grid_search.best_score_}")
print('=' * 60)

# Best CV macro-f1: 0.4982005001600925

print("Training Classification Report:")
print(classification_report(y_train, y_train_pred))

print('=' * 60)

print("Testing Classification Report:")
print(classification_report(y_test, y_pred))

# Training Classification Report:
#               precision    recall  f1-score   support

#            A       0.66      0.72      0.69      1914
#            D       0.70      0.26      0.38      1566
#            H       0.68      0.87      0.76      2944

#     accuracy                           0.67      6424
#    macro avg       0.68      0.61      0.61      6424
# weighted avg       0.68      0.67      0.65      6424

# ============================================================
# Testing Classification Report:
#               precision    recall  f1-score   support

#            A       0.56      0.64      0.60       505
#            D       0.28      0.10      0.14       391
#            H       0.63      0.79      0.70       710

#     accuracy                           0.58      1606
#    macro avg       0.49      0.51      0.48      1606
# weighted avg       0.52      0.58      0.53      1606