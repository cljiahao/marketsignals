# MarketSignal v4

A comprehensive technical analysis and trading signal generation system that combines multiple indicators, candlestick patterns, and market analysis to provide actionable trading signals.

## Features

### 🎯 Multi-Timeframe Analysis

- **Daily & Weekly Analysis**: Combines signals from both daily and weekly timeframes for stronger conviction
- **Signal Aggregation**: Daily and weekly signals are combined using intelligent rules for final decision making

### 📊 Technical Indicators

- **Oscillators**: RSI, MACD, OBV (On-Balance Volume)
- **Overlays**: Moving Average Crossovers, Bollinger Bands, Volume SMA
- **Trend Analysis**: ADX (Average Directional Index) for trend strength
- **Support/Resistance**: Automatic detection and proximity analysis

### 🕯️ Candlestick Pattern Recognition

- **Single Candle Patterns**: Doji, Hammer, Shooting Star, etc.
- **Two Candle Patterns**: Engulfing, Harami, etc.
- **Three Candle Patterns**: Morning Star, Evening Star, Three White Soldiers, etc.

### 🎲 Scoring System

- **Weighted Scoring**: Each indicator contributes with carefully tuned weights
- **ADX Adjustment**: Trend strength modifies signal confidence
- **S/R Proximity**: Distance from support/resistance levels affects signal strength
- **Threshold-Based Decisions**: Clear BUY/SELL/HOLD signals based on score thresholds

### 📈 Backtesting Capabilities

- **Historical Analysis**: Test strategies on historical data
- **Performance Metrics**: Track signal accuracy and profitability
- **Parameter Optimization**: Fine-tune buy/sell thresholds

## Project Structure

```
MarketSignal v4/
├── main.py                 # Main execution script
├── engine.py              # Core signal generation logic
├── backtest.py            # Backtesting functionality
├── data_types/
│   └── signal.py          # Signal data structure
├── indicators/
│   ├── index.py           # Indicator preparation
│   ├── oscillators.py     # RSI, MACD, OBV calculations
│   └── overlays.py        # MA, Bollinger Bands, Volume
├── candle_sticks/
│   ├── index.py           # Candlestick pattern detection
│   ├── single.py          # Single candle patterns
│   ├── two.py             # Two candle patterns
│   ├── three.py           # Three candle patterns
│   ├── conditions.py      # Pattern conditions
│   └── helper.py          # Utility functions
├── scoring/
│   ├── candlesticks.py    # Candlestick pattern scoring
│   ├── oscillators.py     # Oscillator scoring
│   └── overlays.py        # Overlay indicator scoring
├── previews/
│   ├── charts.py          # Chart visualization
│   └── verbose.py         # Detailed signal output
└── utils/
    ├── debug.py           # Debug utilities
    └── helper.py          # General helper functions
```

## Usage

### Basic Usage

```python
python main.py
```

### Supported Markets

- **Singapore Stocks**: REITs and major companies (CRPU.SI, J69U.SI, etc.)
- **US Stocks**: Major tech and blue-chip stocks (AAPL, MSFT, GOOGL, etc.)

### Signal Types

- **BUY**: Strong bullish signal (score ≥ 0.65)
- **SELL**: Strong bearish signal (score ≤ 0.15)
- **HOLD**: Neutral or weak signal

### Signal Components

Each signal includes:

- **Ticker**: Stock symbol
- **Signal**: BUY/SELL/HOLD
- **Reasons**: Detailed explanation of signal components
- **Entry Range**: Suggested entry price range based on ATR
- **Last Close**: Most recent closing price
- **ATR**: Average True Range for volatility assessment

## Technical Details

### Scoring Weights

- **MACD**: 25% (trend/momentum)
- **MA Cross**: 25% (trend)
- **RSI**: 10% (momentum)
- **OBV**: 10% (volume flow)
- **Bollinger Bands**: 10% (volatility/overbought)
- **Volume SMA**: 10% (volume confirmation)
- **Candlesticks**: 10% (pattern recognition)

### Adjustments

- **ADX Factor**:
  - < 20: 0.8x (weak trend)
  - 20-40: 1.0x (normal)
  - > 40: 1.2x (strong trend)
- **S/R Factor**:
  - Near S/R: 1.2x (stronger signal)
  - Far from S/R: 0.8x (weaker signal)

## Requirements

- Python 3.8+
- pandas
- numpy
- yfinance
- matplotlib (for charting)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install pandas numpy yfinance matplotlib
   ```
3. Run the main script:
   ```bash
   python main.py
   ```

## Backtesting

Use the backtesting module to test strategies on historical data:

```python
python backtest.py
```

## Contributing

This is a personal trading signal system. Feel free to fork and modify for your own use.

## Disclaimer

This software is for educational and research purposes only. Trading involves risk, and past performance does not guarantee future results. Always do your own research and consider consulting with a financial advisor before making investment decisions.
