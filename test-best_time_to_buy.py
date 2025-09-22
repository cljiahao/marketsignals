import numpy as np
import yfinance as yf

# 1. Download 5 year of daily prices (Open, Low, Close)
sg_tickers = [
    "U11.SI",
    "O39.SI",
    "D05.SI",
    "BUOU.SI",
    "JYEU.SI",
    "J69U.SI",
    "CRPU.SI",
    "ME8U.SI",
    "M44U.SI",
    "AJBU.SI",
    "A17U.SI",
    "T82U.SI",
    "AIY.SI",
    "OV8.SI",
    "S63.SI",
    "C6L.SI",
    "CJLU.SI",
    "Z74.SI",
    "S68.SI",
    "WJP.SI",
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

tickers = us_tickers + sg_tickers

df = yf.download(tickers, start="2010-01-01", end="2024-12-31")


# --- Helper: week of month (Mon-start) ---
def week_of_month(dt):
    # Monday=0 ... Sunday=6
    first = dt.replace(day=1)
    return int(np.ceil((dt.day + first.weekday()) / 7.0))


# 2. Add week/year/day columns
for price_type in ["Open", "Low", "Close"]:
    df[price_type, "year_week"] = df[price_type].index.to_series().dt.strftime("%Y-%U")
    df[price_type, "day_of_week"] = df[price_type].index.dayofweek
    idx = df[price_type].index
    df[price_type, "year_month"] = idx.to_period("M").astype(str)  # 'YYYY-MM'
    df[price_type, "week_of_month"] = idx.to_series().apply(week_of_month)
    df[price_type, "quarter"] = df[price_type].index.to_series().dt.quarter

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
week_labels = {i: f"Week {i}" for i in range(1, 7)}
month_labels = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}

# 3. Loop through each ticker and calculate lowest days for Open, Low, Close
for ticker in tickers:
    print(f"\n=== {ticker} ===")

    results = {}
    results_wom = {}
    # results_month = {}
    month_per_quarter_results = {}

    for price_type in ["Close", "Open", "Low"]:
        ticker_df = df[price_type][[ticker]].copy()
        ticker_df["year_week"] = df[price_type]["year_week"]
        ticker_df["day_of_week"] = df[price_type]["day_of_week"]
        ticker_df["year_month"] = df[price_type]["year_month"]
        ticker_df["week_of_month"] = df[price_type]["week_of_month"]
        ticker_df["quarter"] = df[price_type]["quarter"]
        ticker_df = ticker_df.dropna()

        # Find the lowest price day per week
        lowest_per_week = ticker_df.loc[
            ticker_df.groupby("year_week")[ticker].idxmin()
        ].reset_index(drop=True)

        # Count how often each weekday is the lowest
        day_counts = lowest_per_week["day_of_week"].value_counts().sort_index()

        # Find the most frequent day
        best_day_idx = day_counts.idxmax()
        best_day_name = days_of_week[best_day_idx]
        best_day_count = day_counts.max()

        second_best_idx = day_counts.nlargest(2).index[-1]
        second_best_day = days_of_week[second_best_idx]
        second_best_day_count = day_counts.nlargest(2).iloc[-1]

        results[price_type] = (
            f"{best_day_name} ({best_day_count} weeks) Second: {second_best_day} ({second_best_day_count} weeks)"
        )

        # Find the single lowest day PER MONTH (e.g., lowest Close in that month)
        lowest_per_month = ticker_df.loc[
            ticker_df.groupby("year_month")[ticker].idxmin()
        ].reset_index(drop=True)

        # Count which week-of-month those lows fell into
        wom_counts = lowest_per_month["week_of_month"].value_counts().sort_index()

        best_wom = wom_counts.idxmax()
        best_wom_name = week_labels.get(int(best_wom), f"Week {int(best_wom)}")
        best_wom_count = int(wom_counts.max())

        # Handle second best safely (if there is more than one unique week)
        if wom_counts.size >= 2:
            top2 = wom_counts.nlargest(2)
            second_best_idx = top2.index[-1]
            second_best_name = week_labels.get(
                int(second_best_idx), f"Week {int(second_best_idx)}"
            )
            second_best_count = int(top2.iloc[-1])
            summary = f"{best_wom_name} ({best_wom_count} months)  Second: {second_best_name} ({second_best_count} months)"
        else:
            summary = f"{best_wom_name} ({best_wom_count} months)"

        results_wom[price_type] = summary

        # # Find the lowest price month per year
        # lowest_per_month["month_num"] = (
        #     lowest_per_month["year_month"].str[5:].astype(int)
        # )
        # lowest_per_month["month_name"] = lowest_per_month["month_num"].map(month_labels)

        # month_counts = lowest_per_month["month_name"].value_counts()
        # best_month = month_counts.idxmax()
        # best_month_count = month_counts.max()

        # if month_counts.size >= 2:
        #     top2_months = month_counts.nlargest(2)
        #     second_month = top2_months.index[-1]
        #     second_month_count = top2_months.iloc[-1]
        #     month_summary = (
        #         f"{best_month} ({best_month_count} times) "
        #         f"Second: {second_month} ({second_month_count} times)"
        #     )
        # else:
        #     month_summary = f"{best_month} ({best_month_count} times)"
        # results_month[price_type] = month_summary

        # --- NEW: Lowest month within each quarter (per year) ---
        monthly_lows = ticker_df.loc[ticker_df.groupby("year_month")[ticker].idxmin()]
        monthly_lows["month_num"] = monthly_lows["year_month"].str[5:].astype(int)
        monthly_lows["month_name"] = monthly_lows["month_num"].map(month_labels)
        monthly_lows["year"] = monthly_lows.index.year
        monthly_lows["quarter"] = monthly_lows.index.to_series().dt.quarter

        lowest_months_per_quarter = monthly_lows.loc[
            monthly_lows.groupby(["year", "quarter"])[ticker].idxmin()
        ]

        summary_list = []
        for q in sorted(lowest_months_per_quarter["quarter"].unique()):
            months_in_q = lowest_months_per_quarter[
                lowest_months_per_quarter["quarter"] == q
            ]
            month_counts = months_in_q["month_name"].value_counts()

            best_month = month_counts.idxmax()
            best_count = month_counts.max()

            if month_counts.size >= 2:
                top2 = month_counts.nlargest(2)
                second_month = top2.index[-1]
                second_count = top2.iloc[-1]
                summary_list.append(
                    f"Q{q}: {best_month} ({best_count} times), Second: {second_month} ({second_count} times)"
                )
            else:
                summary_list.append(f"Q{q}: {best_month} ({best_count} times)")

        month_per_quarter_results[price_type] = summary_list

    # print(f"Lowest Close Day: {results['Close']}")
    # print(f"Lowest Open Day: {results['Open']}")
    print(f"Lowest Low Day: {results['Low']}")

    # print(f"Monthly Lowest Close fell most in: {results_wom['Close']}")
    # print(f"Monthly Lowest Open fell most in: {results_wom['Open']}")
    print(f"Monthly Lowest Low fell most in: {results_wom['Low']}")

    # print(f"Yearly Lowest Close fell most in: {results_month['Close']}")
    # print(f"Yearly Lowest Open fell most in: {results_month['Open']}")
    # print(f"Yearly Lowest Low fell most in: {results_month['Low']}")

    # print(f"Lowest Close month within each quarter: {month_per_quarter_results['Close']}")
    # print(f"Lowest Open month within each quarter: {month_per_quarter_results['Open']}")
    print(f"Lowest Low month within each quarter: {month_per_quarter_results['Low']}")
