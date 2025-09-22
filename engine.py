import numpy as np
import pandas as pd

from data_types.signal import Signal
from scoring.candlesticks import get_candlestick_score
from scoring.oscillators import get_macd_score, get_obv_slope_score, get_rsi_score
from scoring.overlays import get_bb_score, get_ma_cross_score, get_volume_sma20_score


def generate_signal(df: pd.DataFrame) -> Signal:
    reasons = []

    current = df.iloc[-1]
    previous = df.iloc[-2]

    # -----------------------------
    # Oscillators
    rsi_score, rsi_reason = get_rsi_score(current, previous)
    macd_score, macd_reason = get_macd_score(current, previous)
    obv_score, obv_reason = get_obv_slope_score(current, previous)

    # -----------------------------
    # Overlays
    ma_cross_score, ma_cross_reason = get_ma_cross_score(current, previous)
    bollinger_score, bollinger_reason = get_bb_score(current, previous)
    vol_sma20_score, vol_sma20_reason = get_volume_sma20_score(current, previous)

    # -----------------------------
    # Candlesticks patterns
    candle_score, candle_reason = get_candlestick_score(df)

    # -----------------------------
    # ATR-based expected move
    atr_val = float(current["atr"])
    last_close = float(current["Close"])
    entry_low = last_close - 0.5 * atr_val
    entry_high = last_close + 0.8 * atr_val

    # -----------------------------
    # ADX adjustment (0–100 → 0–1 strength)
    adx_val = float(current["adx"])
    adx_strength = adx_val / 100

    # -----------------------------
    # Winshift SNR adjustment
    near_snr = current["snr"]
    if not np.isnan(near_snr):
        tolerance = last_close * 0.05
        dist = abs(last_close - near_snr)
        snr_strength = max(0, 1 - dist / tolerance)

    # -----------------------------
    weights = {
        "rsi": 0.1,  # momentum
        "macd": 0.25,  # trend/momentum
        "obv": 0.1,  # volume flow
        "ma_cross": 0.25,  # trend
        "bollinger": 0.1,  # volatility/overbought
        "volume": 0.1,  # raw volume,
        "candlestick": 0.1,  # candlesticks
    }
    base_score = (
        rsi_score * weights["rsi"]
        + macd_score * weights["macd"]
        + obv_score * weights["obv"]
        + ma_cross_score * weights["ma_cross"]
        + bollinger_score * weights["bollinger"]
        + vol_sma20_score * weights["volume"]
        + candle_score * weights["candlestick"]
    )

    # Apply ADX + SNR multipliers
    if adx_val < 20:
        adx_factor = 0.8
    elif adx_val > 40:
        adx_factor = 1.2
    else:
        adx_factor = 1.0

    if np.isnan(near_snr):
        snr_factor = 1.0
    elif snr_strength > 0.7:
        snr_factor = 1.2
    else:
        snr_factor = 0.8

    adjusted_score = base_score * adx_factor * snr_factor

    # Clamp final score to 0–1
    bullish_score = min(1.0, max(0.0, adjusted_score))

    # -----------------------------
    # Collect reasons
    reasons.extend(
        [
            rsi_reason,
            macd_reason,
            obv_reason,
            ma_cross_reason,
            bollinger_reason,
            vol_sma20_reason,
            candle_reason,
        ]
    )
    if adx_strength > 0.6:
        reasons.append(f"Strong trend (ADX={adx_val:.1f})")
    if not np.isnan(near_snr):
        reasons.append(f"Near S/R level at {near_snr:.2f}")

    # -----------------------------
    # Final decision based on thresholds
    if bullish_score >= 0.65:
        signal = "BUY"
    elif bullish_score <= 0.15:
        signal = "SELL"
    else:
        if candle_score > 0.7:
            signal = "BUY"
        elif candle_score < -0.7:
            signal = "SELL"
        else:
            signal = "HOLD"

    return Signal(
        ticker=df.attrs.get("TICKER", "UNK"),
        signal=signal,
        reasons=reasons,
        entry_range=(round(entry_low, 4), round(entry_high, 4)),
        last_close=round(last_close, 4),
        atr=round(atr_val, 6),
    )
