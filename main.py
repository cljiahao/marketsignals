import pandas as pd
import yfinance as yf

from candle_sticks.index import prepare_candle_sticks
from data_types.signal import Signal
from engine import generate_signal
from indicators.index import prepare_indicators
from previews.verbose import print_signals_multi_tf

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


def prepare_df(df: pd.DataFrame):
    df = df.reset_index()
    df = prepare_indicators(df)
    return prepare_candle_sticks(df)


def main():

    tickers = sg_tickers + us_tickers

    df_daily = yf.download(
        tickers, period="2y", interval="1d", group_by="ticker", auto_adjust=True
    )
    df_weekly = yf.download(
        tickers, period="5y", interval="1wk", group_by="ticker", auto_adjust=True
    )

    results = []

    for ticker in tickers:
        prep_daily_df = prepare_df(df_daily[ticker])
        prep_weekly_df = prepare_df(df_weekly[ticker])

        sig_daily = generate_signal(prep_daily_df)
        sig_weekly = generate_signal(prep_weekly_df)

        # Combine signals (simple rule: both need to be BUY for strong BUY)
        if sig_daily.signal == "BUY" and sig_weekly.signal == "BUY":
            final_signal = "BUY"
        elif sig_daily.signal == "SELL" and sig_weekly.signal == "SELL":
            final_signal = "SELL"
        else:
            final_signal = "HOLD"

        combined = Signal(
            short_name=yf.Ticker(ticker).info.get("shortName", ticker),
            ticker=ticker,
            signal=final_signal,
            reasons=[f"Daily: {sig_daily.signal}", f"Weekly: {sig_weekly.signal}"],
            entry_range=sig_weekly.entry_range,
            last_close=sig_daily.last_close,
            atr=sig_weekly.atr,
        )

        results.append({"daily": sig_daily, "weekly": sig_weekly, "combined": combined})

    print_signals_multi_tf(results, scores_only=True)


if __name__ == "__main__":
    main()
