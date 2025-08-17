from typing import Any, Dict
from utils.api import AlphaVantageAPI
from utils.data_model import market_data_cache, MarketData
from utils.indicators import sma
from datetime import datetime

# def calculate_moving_averages(symbol: str, short_period: int = 20, long_period: int = 50):
#     cache_key = f"{symbol}_1min"
#     if cache_key not in market_data_cache:
#         df = AlphaVantageAPI.get_intraday_data(symbol, "1min", "full")
#         market_data_cache[cache_key] = MarketData(symbol, "1min", df, datetime.now())

#     data = market_data_cache[cache_key].data
#     data[f"SMA{short_period}"] = sma(data['close'], short_period)
#     data[f"SMA{long_period}"] = sma(data['close'], long_period)

#     latest = data.iloc[-1]
#     short_ma = latest[f"SMA{short_period}"]
#     long_ma = latest[f"SMA{long_period}"]

#     signal = "BULLISH" if short_ma > long_ma else "BEARISH" if short_ma < long_ma else "NEUTRAL"

#     return {
#         "symbol": symbol,
#         "current_price": latest['close'],
#         f"SMA{short_period}": short_ma,
#         f"SMA{long_period}": long_ma,
#         "signal": signal,
#         "analysis": f"{short_period}-SMA vs {long_period}-SMA → {signal}"
#     }


def calculate_moving_averages(symbol: str, short_period: int = 20, long_period: int = 50) -> Dict[str, Any]:
    """
    Calculate short and long moving averages for a symbol
    
    Args:
        symbol: The ticker symbol to analyze
        short_period: Short moving average period in minutes
        long_period: Long moving average period in minutes
        
    Returns:
        Dictionary with moving average data and analysis
    """
    cache_key = f"{symbol}_1min"
    
    if cache_key not in market_data_cache:
        df = AlphaVantageAPI.get_intraday_data(symbol, "1min", outputsize="full")
        market_data_cache[cache_key] = MarketData(
            symbol=symbol,
            interval="1min",
            data=df,
            last_updated=datetime.now()
        )
    
    data = market_data_cache[cache_key].data
    
    # Calculate moving averages
    data[f'SMA{short_period}'] = data['close'].rolling(window=short_period).mean()
    data[f'SMA{long_period}'] = data['close'].rolling(window=long_period).mean()
    
    # Get latest values
    latest = data.iloc[-1]
    current_price = latest['close']
    short_ma = latest[f'SMA{short_period}']
    long_ma = latest[f'SMA{long_period}']
    
    # Determine signal
    if short_ma > long_ma:
        signal = "BULLISH (Short MA above Long MA)"
    elif short_ma < long_ma:
        signal = "BEARISH (Short MA below Long MA)"
    else:
        signal = "NEUTRAL (MAs are equal)"
    
    # Check for crossover in the last 5 periods
    last_5 = data.iloc[-5:]
    crossover = False
    crossover_type = ""
    
    for i in range(1, len(last_5)):
        prev = last_5.iloc[i-1]
        curr = last_5.iloc[i]
        
        # Golden Cross (short crosses above long)
        if prev[f'SMA{short_period}'] <= prev[f'SMA{long_period}'] and curr[f'SMA{short_period}'] > curr[f'SMA{long_period}']:
            crossover = True
            crossover_type = "GOLDEN CROSS (Bullish)"
            break
            
        # Death Cross (short crosses below long)
        if prev[f'SMA{short_period}'] >= prev[f'SMA{long_period}'] and curr[f'SMA{short_period}'] < curr[f'SMA{long_period}']:
            crossover = True
            crossover_type = "DEATH CROSS (Bearish)"
            break
    
    return {
        "symbol": symbol,
        "current_price": current_price,
        f"SMA{short_period}": short_ma,
        f"SMA{long_period}": long_ma,
        "signal": signal,
        "crossover_detected": crossover,
        "crossover_type": crossover_type if crossover else "None",
        "analysis": f"""Moving Average Analysis for {symbol}:
Current Price: ${current_price:.2f}
{short_period}-period SMA: ${short_ma:.2f}
{long_period}-period SMA: ${long_ma:.2f}
Signal: {signal}
Recent Crossover: {"Yes - " + crossover_type if crossover else "No"}

Recommendation: {
    "STRONG BUY" if crossover and crossover_type == "GOLDEN CROSS (Bullish)" else
    "BUY" if signal == "BULLISH (Short MA above Long MA)" else
    "STRONG SELL" if crossover and crossover_type == "DEATH CROSS (Bearish)" else
    "SELL" if signal == "BEARISH (Short MA below Long MA)" else
    "HOLD"
}"""
 }
 