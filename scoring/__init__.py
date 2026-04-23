import pandas as pd

from data_types.score import ScoreReason
from scoring.oscillators import get_macd_score, get_obv_slope_score, get_rsi_score
from scoring.overlays import get_bb_score, get_ma_cross_score, get_volume_sma20_score


def compute_component_base(current: pd.Series, previous: pd.Series) -> ScoreReason:
    """
    Compute raw component scores for the given row pair.
    Returns dict {indicator: (score, reason)}
    """
    rsi_score, rsi_reason = get_rsi_score(current, previous)
    macd_score, macd_reason = get_macd_score(current, previous)
    obv_score, obv_reason = get_obv_slope_score(current, previous)
    ma_cross_score, ma_cross_reason = get_ma_cross_score(current, previous)
    bollinger_score, bollinger_reason = get_bb_score(current, previous)
    vol_sma20_score, vol_sma20_reason = get_volume_sma20_score(current, previous)

    return {
        "rsi": ScoreReason(score=rsi_score, reason=rsi_reason),
        "macd": ScoreReason(score=macd_score, reason=macd_reason),
        "obv": ScoreReason(score=obv_score, reason=obv_reason),
        "ma_cross": ScoreReason(score=ma_cross_score, reason=ma_cross_reason),
        "bollinger": ScoreReason(score=bollinger_score, reason=bollinger_reason),
        "volume": ScoreReason(score=vol_sma20_score, reason=vol_sma20_reason),
    }
