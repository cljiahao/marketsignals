import numpy as np
import pandas as pd
import yfinance as yf

from scoring.candlesticks import get_candlestick_score
from scoring.oscillators import get_macd_score, get_obv_slope_score, get_rsi_score
from scoring.overlays import get_bb_score, get_ma_cross_score, get_volume_sma20_score
from test import prepare_df


def generate_signals_backtest(
    df: pd.DataFrame, buy: float, sell: float
) -> pd.DataFrame:
    """
    Generate bullish_score and signal for each row in the dataframe.
    """
    df = df.copy()
    df["bullish_score"] = np.nan
    df["signal"] = "HOLD"

    # Candlesticks patterns
    candle_score, _ = get_candlestick_score(df)

    for i in range(1, len(df)):
        current = df.iloc[i]
        previous = df.iloc[i - 1]

        # Oscillators
        rsi_score, _ = get_rsi_score(current, previous)
        macd_score, _ = get_macd_score(current, previous)
        obv_score, _ = get_obv_slope_score(current, previous)

        # Overlays
        ma_cross_score, _ = get_ma_cross_score(current, previous)
        bollinger_score, _ = get_bb_score(current, previous)
        vol_sma20_score, _ = get_volume_sma20_score(current, previous)

        # Base score weighted
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

        # ATR-based expected move
        last_close = float(current["Close"])

        # -----------------------------
        # ADX adjustment (0–100 → 0–1 strength)
        adx_val = float(current["adx"])

        # -----------------------------
        # Winshift SNR adjustment
        near_snr = current["snr"]
        if not np.isnan(near_snr):
            tolerance = last_close * 0.05
            dist = abs(last_close - near_snr)
            snr_strength = max(0, 1 - dist / tolerance)

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

        # Save
        df.at[i, "bullish_score"] = bullish_score
        if bullish_score >= buy:
            df.at[i, "signal"] = "BUY"
        elif bullish_score <= sell:
            df.at[i, "signal"] = "SELL"
        else:
            if candle_score > 0.7:
                df.at[i, "signal"] = "BUY"
            elif candle_score < -0.7:
                df.at[i, "signal"] = "SELL"
            else:
                df.at[i, "signal"] = "HOLD"

    return df


sg_tickers = [
    "CRPU.SI",
    "J69U.SI",
    "BUOU.SI",
    "M44U.SI",
    "ME8U.SI",
    "JYEU.SI",
    "AJBU.SI",
    "DCRU.SI",
    "U11.SI",
    "C6L.SI",
    "CJLU.SI",
    "O39.SI",
]

us_tickers = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "NVDA",
    "AMZN",
    "BABA",
    "V",
    "MA",
    "JPM",
    "JNJ",
    "META",
]

tickers = us_tickers

df_daily = yf.download(
    tickers, period="2y", interval="1d", group_by="ticker", auto_adjust=True
)
df_weekly = yf.download(
    tickers, period="5y", interval="1wk", group_by="ticker", auto_adjust=True
)

average_buy_range = 0
average_sell_range = 0

for ticker in tickers:
    df = prepare_df(df_daily[ticker])
    df = df.reset_index()

    best_result = {
        "buy_range": 0.0,
        "sell_range": 1.0,
        "max equity": 0,
        "latest equity": 0,
    }

    for buy in np.linspace(0.6, 1.0, 9):
        for sell in np.linspace(0.4, 0.0, 9):
            if sell >= buy:
                continue

            df = generate_signals_backtest(df, buy, sell)

            capital = 100000
            position = 0
            equity_curve = []

            for i, row in df.iterrows():
                if row["signal"] == "BUY" and position == 0:
                    entry_price = row["Close"]
                    position = capital / entry_price
                elif row["signal"] == "SELL" and position > 0:
                    capital = position * row["Close"]
                    position = 0
                equity_curve.append(
                    capital if position == 0 else position * row["Close"]
                )

            df["equity"] = equity_curve
            max_equity = df["equity"].max()

            if best_result["max equity"] < max_equity:
                best_result = {
                    "buy_range": buy,
                    "sell_range": sell,
                    "max equity": max_equity,
                    "latest equity": df["equity"].iloc[-1],
                }
            elif best_result["max equity"] == max_equity:
                best_result = {
                    "buy_range": max(buy, best_result.get("buy_range", buy)),
                    "sell_range": min(sell, best_result.get("sell_range", sell)),
                    "max equity": max_equity,
                    "latest equity": df["equity"].iloc[-1],
                }
    average_buy_range += best_result["buy_range"]
    average_sell_range += best_result["sell_range"]
    print(f"Ticker: {ticker} {best_result}")

print("")
print(
    f"Buy range: {average_buy_range / len(tickers)}, Sell range: {average_sell_range / len(tickers)}"
)
