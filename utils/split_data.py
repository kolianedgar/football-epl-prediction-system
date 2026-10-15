def split_data_features_targets(df, date_column, columns_to_drop, target_column):

    df = df.copy()

    columns_to_check = columns_to_drop + [date_column, target_column]

    for col in columns_to_check:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in the DataFrame")

    if target_column in columns_to_drop:
        raise ValueError(f"Target column {target_column} must not be in columns_to_drop")
    
    df_chronological = (
        df.sort_values(date_column)
            .reset_index(drop=True)
    )

    X_chronological = df_chronological.drop(
        columns = list(columns_to_drop + [date_column, target_column])
    )

    y_chronological = df_chronological[target_column].copy()

    return X_chronological, y_chronological

def split_df_train_test(X, y, split_proportion):
    split_idx = int(len(X) * split_proportion)

    X_train = X.iloc[:split_idx].copy()
    X_test = X.iloc[split_idx:].copy()

    y_train = y.iloc[:split_idx].copy()
    y_test = y.iloc[split_idx:].copy()

    return X_train, X_test, y_train, y_test