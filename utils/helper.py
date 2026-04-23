import numpy as np
import pandas as pd


def require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")


def last_valid(series: pd.Series) -> float:
    # Get last non-NaN value
    if series.dropna().empty:
        raise ValueError(f"Series '{series.name}' has no valid values.")
    return float(series.dropna().iat[-1])


def zscale(x: float) -> float:
    """Map [0,1] -> [-1,1] for uniform combination."""
    return (float(x) - 0.5) * 2.0


def rescale_to_unit(x: float) -> float:
    """Map [-1,1] -> [0,1] after combination."""
    return float(np.clip((x + 1.0) / 2.0, 0.0, 1.0))
