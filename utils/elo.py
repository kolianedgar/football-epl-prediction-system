def add_elo_columns_to_dataframe(
    df,
    home_team_col = None,
    away_team_col = None,
    fthg = None,
    ftag = None,
    ftr = None,
    initial_elo=1500,
    home_advantage=50
):

    columns_to_check = [home_team_col, away_team_col, fthg, ftag, ftr]
    for col in columns_to_check:
        if col is None:
            raise ValueError(f"Column {col} is None!")
        
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in the dataframe!")
        
    df = df.copy()
    df["_original_order"] = range(len(df))

    ratings = {}
    home_team_features = []
    away_team_features = []

    for _, row in df.iterrows():
        home_team = row[home_team_col]
        away_team = row[away_team_col]

        home_elo = ratings.get(home_team, initial_elo)
        away_elo = ratings.get(away_team, initial_elo)

        home_team_features.append(home_elo)
        away_team_features.append(away_elo)

        new_home_elo, new_away_elo = _calculate_elo(
            ftr=row[ftr],
            fthg=row[fthg],
            ftag=row[ftag],
            home_elo = home_elo,
            away_elo=away_elo,
            home_advantage=home_advantage
        )

        ratings[home_team] = new_home_elo
        ratings[away_team] = new_away_elo

    df["HomeElo"] = home_team_features
    df["AwayElo"] = away_team_features

    df["EloDifference"] = df["HomeElo"] - df["AwayElo"]
    df = (
        df.sort_values("_original_order").drop(columns="_original_order")
    )

    return df

def _calculate_elo(
    ftr,
    fthg,
    ftag,
    home_elo,
    away_elo,
    home_advantage
):

    if ftr not in ['H', 'A', 'D']:
        raise ValueError(f"Full-time result {ftr} is invalid")

    goal_difference = abs(fthg - ftag)
    gd_multiplier = _calculate_goal_difference_multiplier(goal_difference)

    k_efficient = 30 * gd_multiplier

    home_score = _calculate_home_score(ftr)
    home_expected_score = _calculate_expected_home_score(home_elo, away_elo, home_advantage)
    
    post_match_home_elo = _calculate_elo_after_match(
        mode='H',
        home_elo_before=home_elo,
        away_elo_before=away_elo,
        k=k_efficient,
        score_home=home_score,
        score_expected_home=home_expected_score
    )

    post_match_away_elo = _calculate_elo_after_match(
        mode='A',
        home_elo_before=home_elo,
        away_elo_before=away_elo,
        k=k_efficient,
        score_home=home_score,
        score_expected_home=home_expected_score
    )

    return post_match_home_elo, post_match_away_elo

def _calculate_goal_difference_multiplier(goal_difference):
    if goal_difference == 0 or goal_difference == 1:
        return 1
    elif goal_difference == 2:
        return 1.5
    elif goal_difference == 3:
        return 1.75
    elif goal_difference >= 4:
        return 1.75 + ((goal_difference - 3)/8)

def _calculate_home_score(ftr):

    if ftr == 'H':
        return 1
    elif ftr == 'D':
        return 0.5
    elif ftr == 'A':
        return 0

def _calculate_expected_home_score(elo_home, elo_away, home_advantage):
    return 1/(1 + (10**(-(elo_home + home_advantage - elo_away)/400)))

def _calculate_elo_after_match(mode, home_elo_before, away_elo_before, k, score_home, score_expected_home):

    if mode not in ["Home", "Away", 'H', 'A']:
        raise ValueError(f"Mode {mode} is invalid")
    
    if mode == "Home" or mode == 'H':
        return home_elo_before + k * (score_home - score_expected_home)

    if mode == "Away" or mode == 'A':
        return away_elo_before - k * (score_home - score_expected_home)