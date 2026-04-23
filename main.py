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

    for region, tickers in {"SG": sg_tickers, "US": us_tickers}.items():

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

            # Combine signals
            combined_confidence = (
                0.6 * sig_daily.confidence + 0.4 * sig_weekly.confidence
            )

            # Map combined confidence to final signal
            if combined_confidence >= 0.75:
                final_signal = "STRONG BUY"
            elif combined_confidence >= 0.60:
                final_signal = "BUY"
            elif combined_confidence <= 0.25:
                final_signal = "STRONG SELL"
            elif combined_confidence <= 0.40:
                final_signal = "SELL"
            else:
                final_signal = "HOLD"

            combined = Signal(
                short_name=yf.Ticker(ticker).info.get("shortName", ticker),
                ticker=ticker,
                signal=final_signal,
                confidence=round(combined_confidence, 4),
                reasons=[f"Daily: {sig_daily.signal}", f"Weekly: {sig_weekly.signal}"],
                entry_range=sig_weekly.entry_range,
                last_close=sig_daily.last_close,
                atr=sig_weekly.atr,
            )

            results.append(
                {"daily": sig_daily, "weekly": sig_weekly, "combined": combined}
            )

        print_signals_multi_tf(results, region, scores_only=False)


if __name__ == "__main__":
    main()
