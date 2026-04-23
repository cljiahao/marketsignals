from dataclasses import dataclass


@dataclass
class Signal:
    ticker: str
    signal: str  # STRONG BUY / BUY / HOLD / SELL / STRONG SELL
    confidence: float  # [0.0, 1.0]
    reasons: list[str]
    entry_range: tuple[float, float]  # (low, high)
    last_close: float
    atr: float
    short_name: str = ""
