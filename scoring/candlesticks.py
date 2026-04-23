import numpy as np
import pandas as pd


def get_candlestick_score(df: pd.DataFrame, atr_val: float = 1.0) -> tuple[float, str]:
    """
    Compute a candlestick score scaled by volatility (ATR) with decay over lookback_days.
    Returns a continuous score in [-1,1] and a human-readable reason.
    """
    lookback_days = 30
    base_decay = 0.95  # default decay per day

    candle_score = 0.0
    pattern_types = df.attrs.get("pattern_types", {})
    contributing_patterns = []

    for i in range(1, lookback_days + 1):
        if i > len(df):
            break
        row = df.iloc[-i]
        days_ago = i - 1

        # Adaptive decay: slightly slower for volatile stocks
        decay_factor = base_decay ** (
            days_ago * (1 + atr_val / max(float(row.get("Close", 1)), 1e-8))
        )

        for col in df.columns:
            if col not in pattern_types:
                continue
            signal_value = row[col]
            if signal_value == 0:
                continue

            # Determine polarity
            polarity = 1 if "bull" in col else -1 if "bear" in col else 0
            candle_score += polarity * signal_value * decay_factor / max(atr_val, 1e-8)

            contributing_patterns.append(col)

    # Normalize to [-1,1]
    score = np.clip(candle_score / 6, -1.0, 1.0)

    # Trend label
    if score > 0.7:
        trend = "Strong Bullish"
    elif score < -0.7:
        trend = "Strong Bearish"
    else:
        trend = "Neutral"

    # Reason: include all contributing patterns
    label = ", ".join(contributing_patterns[-3:])  # last 3 patterns for brevity
    reason = f"{trend} Candlesticks {score:.2f} : {label}"
    return score, reason
