import pandas as pd
from sklearn.feature_selection import mutual_info_classif
import yfinance as yf

from main import prepare_df
from previews.charts import plot_ohlc_chart


df_daily = yf.download(
    "AAPL", period="5y", interval="1wk", group_by="ticker", auto_adjust=True
)

prep_daily_df = prepare_df(df_daily["AAPL"])

# plot_ohlc_chart(prep_daily_df)

test_signal = {
    10: "Sell",
    16: "Buy",
    28: "Strong Buy",
    42: "Sell",
    46: "Buy",
    59: "Sell",
    62: "Buy",
    69: "Buy",
    72: "Strong Sell",
    82: "Buy",
    91: "Strong Sell",
    111: "Strong Buy",
    141: "Sell",
    154: "Buy",
    161: "Sell",
    178: "Buy",
    180: "Strong Buy",
    192: "Sell",
    207: "Buy",
    214: "Sell",
    223: "Strong Sell",
    229: "Buy",
}

prep_daily_df.loc[list(test_signal.keys()), "Signal"] = list(test_signal.values())

# Prepare features (X) and target (y)
X = prep_daily_df.copy()
y = X.pop("Signal")
X = X.select_dtypes(exclude=["datetime64"])  # remove datetime columns
X = X.fillna("Hold")

# Factorize any object-type features in X
for colname in X.select_dtypes("object"):
    X[colname], _ = X[colname].factorize()

# Identify discrete features (integers)
discrete_features = X.dtypes == int

# Compute mutual information (classification, since target is categorical)
mi_scores = mutual_info_classif(X, y, discrete_features=discrete_features)

# Convert to pandas Series for readability
mi_scores = pd.Series(mi_scores, index=X.columns, name="MI Score")
mi_scores = mi_scores.sort_values(ascending=False)

# Show a few features with their MI scores
print(mi_scores)


# 1 if Buy or Strong Buy, 0 otherwise
y_buy = prep_daily_df["Signal"].apply(lambda x: 1 if x in ["Buy", "Strong Buy"] else 0)

# Keep only numeric columns
X_numeric = X.select_dtypes(include=["float64", "int64"])

# Pearson correlation
corr_with_buy = X_numeric.corrwith(y_buy)
corr_with_buy = corr_with_buy.sort_values(ascending=False)
print(corr_with_buy.head(10))
