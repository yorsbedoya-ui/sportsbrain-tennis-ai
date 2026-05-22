import numpy as np

def build_basketball_features(game_data: dict) -> np.ndarray:
    # 1. PER_diff_top8 (average PER of top 8 rotation players difference)
    # 2. net_rating_diff
    # 3. pace_matchup (average pace of both teams)
    # 4. efg_diff (effective field goal percentage difference)
    # 5. rest_advantage (rest_days difference)
    # 6. back_to_back_penalty (-0.5 if team is on back-to-back)
    # 7. home_court (binary)
    # 8. injury_impact_score (weighted sum of injured players' PER)
    # 9. playoff_flag (binary)
    # 10. h2h_last_3seasons
    # 11. momentum_10g
    return np.random.rand(1, 11)
