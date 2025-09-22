import os
<<<<<<< HEAD
=======
from matplotlib.gridspec import GridSpec
>>>>>>> v3
import matplotlib.pyplot as plt
from datetime import datetime as dt

from mplfinance.original_flavor import candlestick_ohlc


class Chart:
<<<<<<< HEAD
    def __init__(self, df, levels, indi, candles, ticker, perInt):
=======
    def __init__(self, df, levels, indi, candles, filePath):
>>>>>>> v3
        self.df = df
        self.indi = indi
        self.levels = levels
        self.candles = candles
<<<<<<< HEAD
        self.ticker = ticker
        self.perInt = perInt
=======
        self.filePath = filePath
>>>>>>> v3
        self.dirpath = os.path.dirname(__file__)
        self.plot()

    def plot(self):

        plt.ioff()

<<<<<<< HEAD
        ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1, sharex=ax1)
=======
        fig = plt.figure(figsize=(20, 10))
        gs = GridSpec(3, 1, height_ratios=[2, 1, 0], hspace=0)  # 2/3 and 1/3 ratio
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
>>>>>>> v3

        candlestick_ohlc(
            ax1, self.df.values, width=0.7, colorup="green", colordown="red", alpha=0.8
        )

        for level in self.levels:
            ax1.hlines(
                level[1],
                xmin=min(self.df["Date"]),
                xmax=max(self.df["Date"]),
                colors="blue",
                linestyle="--",
                alpha=0.3,
            )

        ax1.scatter(
            x=self.df["Date"], y=self.df["Buy"] * 0.99, s=30, c="green", marker="^"
        )
        ax1.scatter(
            x=self.df["Date"], y=self.df["Sell"] * 1.01, s=30, c="red", marker="v"
        )

<<<<<<< HEAD
=======
        # ax1.scatter(x=self.df["Date"],y=self.df["minSP"]*0.98,s=20,c="green",marker="D")
        # ax1.scatter(x=self.df["Date"],y=self.df["maxSP"]*1.02,s=20,c="red",marker="D")

>>>>>>> v3
        # Market Downturn
        ax1.scatter(
            x=self.df["Date"], y=self.df["Correction"], s=30, c="blue", marker="d"
        )
        ax1.scatter(
            x=self.df["Date"], y=self.df["Recession"], s=30, c="green", marker="d"
        )
        ax1.scatter(x=self.df["Date"], y=self.df["Crash"], s=30, c="red", marker="d")

        ax1 = self.scatterPlot(ax1)

        for i in self.indi.keys():
            if i.upper() == "SMA":
                for j in self.indi[i]:
                    self.df[f'{i}_{j["length"]}'].plot(ax=ax1)

            elif i.upper() == "MACD":
                ax2.plot(
                    self.df[
                        f"MACD_{self.indi['MACD'][0]['fast']}_{self.indi['MACD'][0]['slow']}_{self.indi['MACD'][0]['signal']}"
                    ],
                    color="grey",
                    linewidth=1.5,
                    label="MACD",
                )
                ax2.plot(
                    self.df[
                        f"MACDs_{self.indi['MACD'][0]['fast']}_{self.indi['MACD'][0]['slow']}_{self.indi['MACD'][0]['signal']}"
                    ],
                    color="skyblue",
                    linewidth=1.5,
                    label="SIGNAL",
                )

                for i in range(len(self.df["Close"])):
                    if (
                        str(
                            self.df[
                                f"MACDh_{self.indi['MACD'][0]['fast']}_{self.indi['MACD'][0]['slow']}_{self.indi['MACD'][0]['signal']}"
                            ][i]
                        )[0]
                        == "-"
                    ):
                        ax2.bar(
                            self.df["Close"].index[i],
                            self.df[
                                f"MACDh_{self.indi['MACD'][0]['fast']}_{self.indi['MACD'][0]['slow']}_{self.indi['MACD'][0]['signal']}"
                            ][i],
                            color="#ef5350",
                        )
                    else:
                        ax2.bar(
                            self.df["Close"].index[i],
                            self.df[
                                f"MACDh_{self.indi['MACD'][0]['fast']}_{self.indi['MACD'][0]['slow']}_{self.indi['MACD'][0]['signal']}"
                            ][i],
                            color="#26a69a",
                        )

<<<<<<< HEAD
        plt.tight_layout()
        plt.get_current_fig_manager().window.state("zoomed")
        plt.show(block=False)
        plt.pause(1)

=======
>>>>>>> v3
        folder = dt.strptime(dt.now().strftime("%Y-W%W") + "-1", "%G-W%V-%u").strftime(
            "%d-%b-%Y"
        )
        folpath = os.path.join(self.dirpath, "images", folder)
        if not os.path.exists(folpath):
            os.makedirs(folpath)
<<<<<<< HEAD
        date = self.df[-1:].index[0].strftime("%d-%m-%Y")
        plt.savefig(
            os.path.join(folpath, date + "_" + self.ticker + "_" + self.perInt + ".png")
=======
        plt.savefig(
            self.filePath,
            dpi=300,
            bbox_inches="tight",
>>>>>>> v3
        )

    def scatterPlot(self, ax1):
        size = 15
        up, down = 1.02, 0.98
        for c in self.candles:
            if c == "Hammers":
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["hammer"] * down,
                    s=size,
                    c="blue",
                    marker="*",
                )
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["invhammer"] * down,
                    s=size,
                    c="blue",
                    marker="*",
                )
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["hanging"] * up,
                    s=size,
                    c="purple",
                    marker="*",
                )
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["shooting"] * up,
                    s=size,
                    c="purple",
                    marker="*",
                )
            elif c == "Stars":
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["morning"] * down,
                    s=size,
                    c="blue",
                    marker="*",
                )
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["evening"] * up,
                    s=size,
                    c="purple",
                    marker="*",
                )
            elif c == "ThreeLineStrike":
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["BullTLS"] * down,
                    s=size,
                    c="blue",
                    marker="*",
                )
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["BearTLS"] * up,
                    s=size,
                    c="purple",
                    marker="*",
                )
            elif c == "RiseNFall":
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["rising"] * down,
                    s=size,
                    c="blue",
                    marker="*",
                )
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["falling"] * up,
                    s=size,
                    c="purple",
                    marker="*",
                )
            elif c == "Engulfing":
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["bullEngulf"] * down,
                    s=size,
                    c="blue",
                    marker="*",
                )
                ax1.scatter(
                    x=self.df["Date"],
                    y=self.df["bearEngulf"] * up,
                    s=size,
                    c="purple",
                    marker="*",
                )

        return ax1
