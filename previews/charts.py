import matplotlib.pyplot as plt
import pandas as pd


def plot_ohlc_chart(df: pd.DataFrame):
    """
    Plot an OHLC candlestick chart.

    Expects df to have columns: Date, Open, High, Low, Close
    """
    df.index = pd.to_datetime(df["Date"])

    plt.figure(figsize=(12, 6))

    # Width of candlestick
    width = 3

    # Up and down colors
    up = df[df["Close"] > df["Open"]]
    down = df[df["Close"] < df["Open"]]
    doji = df[df["Close"] == df["Open"]]

    # Plot high-low lines
    plt.vlines(df.index, df["Low"], df["High"], color="black", linewidth=0.5, zorder=1)

    # Plot up candlesticks (green)
    plt.bar(
        up.index,
        up["Close"] - up["Open"],
        width,
        bottom=up["Open"],
        color="green",
    )

    # Plot down candlesticks (red)
    plt.bar(
        down.index,
        down["Close"] - down["Open"],
        width,
        bottom=down["Open"],
        color="red",
    )

    # Plot doji candlesticks (black)
    plt.bar(
        doji.index,
        1,
        width,
        bottom=doji["Open"],
        color="black",
    )

    plt.title("OHLC Candlestick Chart")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
