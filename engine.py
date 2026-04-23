import numpy as np
import pandas as pd

from data_types.signal import Signal
from scoring import compute_component_base
from scoring.candlesticks import get_candlestick_score
from utils.helper import rescale_to_unit, zscale


def generate_signal(df: pd.DataFrame) -> Signal:

    # -----------------------------
    # Settings
    SMOOTH_WINDOW = 5  # short-term memory of past composite scores

    # Component weights
    weights = {
        "rsi": 0.10,
        "macd": 0.20,
        "ma_cross": 0.15,
        "obv": 0.10,
        "volume": 0.10,
        "bollinger": 0.15,
        "candlestick": 0.20,
    }

    # -----------------------------
    n = len(df)
    start_idx = max(1, n - SMOOTH_WINDOW)
    composite_list = []

    # Compute rolling composite (memory)
    for i in range(start_idx, n):
        current = df.iloc[i]
        previous = df.iloc[i - 1]
        comps = compute_component_base(current, previous)
        # Z-scale all indicators except candlestick
        z_comb = sum(
            zscale(comps[k].score) * w for k, w in weights.items() if k != "candlestick"
        )
        composite_list.append(z_comb)

    composite_mean = float(np.mean(composite_list)) if composite_list else 0.0

    # -----------------------------
    last_close = float(current.get("Close", np.nan))
    atr_val = float(current.get("atr", 0.0) or 0.0)

    # Candlestick tactical weighting
    candle_score, candle_reason = get_candlestick_score(df, atr_val)
    z_candle = zscale(candle_score)
    candle_tactical_weight = 0.6
    composite_with_candle = composite_mean * (
        1.0 - (weights["candlestick"] * candle_tactical_weight)
    ) + z_candle * (weights["candlestick"] * candle_tactical_weight)

    base_bullish_score = rescale_to_unit(composite_with_candle)

    # -----------------------------
    # ADX + SNR contextual multipliers
    adx_val = float(current.get("adx", 0.0) or 0.0)
    adx_strength = adx_val / 100.0
    near_snr = current.get("snr", np.nan)

    snr_strength = 0.0
    if not np.isnan(near_snr):
        dist = abs(last_close - near_snr)

        # Hybrid tolerance for SG + US market compatibility
        price_tol = last_close * 0.02  # 2%
        atr_tol = atr_val * 1.5  # 1.5 ATR range
        tolerance = max(price_tol, atr_tol)  # Choose the more realistic zone

        snr_strength = max(0.0, 1.0 - dist / tolerance)

    # --- Adjustments ---
    adx_factor = 1 + np.clip((adx_strength - 0.4), -0.1, 0.1)
    snr_factor = 1 + (0.15 * snr_strength)
    adjusted_score = float(
        np.clip(base_bullish_score * adx_factor * snr_factor, 0.0, 1.0)
    )

    # -----------------------------
    # Continuous confidence combination
    # Candle score contributes to final confidence
    final_confidence = 0.6 * adjusted_score + 0.4 * np.clip(
        (candle_score + 1) / 2, 0.0, 1.0
    )

    # Map confidence to clear signals
    if final_confidence >= 0.75:
        signal = "STRONG BUY"
    elif final_confidence >= 0.60:
        signal = "BUY"
    elif final_confidence <= 0.25:
        signal = "STRONG SELL"
    elif final_confidence <= 0.40:
        signal = "SELL"
    else:
        signal = "HOLD"

    # # --- Dynamic thresholds (based on volatility) ---
    # vol_factor = (
    #     min(atr_val / max(last_close, 1e-8), 0.05)
    #     if last_close < 100
    #     else min(atr_val / max(last_close, 1e-8), 0.03)
    # )
    # buy_thresh = float(np.clip(0.65 - 0.3 * vol_factor, 0.55, 0.70))
    # sell_thresh = float(np.clip(0.35 + 0.3 * vol_factor, 0.30, 0.45))

    # # Optional soft volatility filter
    # if vol_factor > 0.05:  # too volatile
    #     if signal in ["BUY", "STRONG BUY"]:
    #         signal = "HOLD"
    #     elif signal in ["SELL", "STRONG SELL"]:
    #         signal = "HOLD"

    # -----------------------------
    # Collect reasons
    reasons = [f"{v.reason}" for v in comps.values()]
    reasons.append(f"{candle_reason}")
    if adx_strength > 0.6:
        reasons.append(f"Strong trend (ADX={adx_val:.1f})")
    if not np.isnan(near_snr):
        reasons.append(f"Near S/R level at {near_snr:.2f}")

    # Entry range
    entry_low = last_close - 0.5 * atr_val
    entry_high = last_close + 0.8 * atr_val

    return Signal(
        ticker=df.attrs.get("TICKER", "UNK"),
        signal=signal,
        confidence=round(final_confidence, 4),
        reasons=reasons,
        entry_range=(round(entry_low, 4), round(entry_high, 4)),
        last_close=round(last_close, 4),
        atr=round(atr_val, 6),
    )
