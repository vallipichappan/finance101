from typing import Any, Dict
from tools.moving_average import calculate_moving_averages
from tools.rsi import calculate_rsi


def trade_recommendation(symbol: str) -> Dict[str, Any]:
    """
    Provide a comprehensive trade recommendation based on multiple indicators
    
    Args:
        symbol: The ticker symbol to analyze
        
    Returns:
        Dictionary with trading recommendation and supporting data
    """
    # Calculate individual indicators
    ma_data = calculate_moving_averages(symbol)
    rsi_data = calculate_rsi(symbol)
    
    # Extract signals
    ma_signal = ma_data["signal"]
    ma_crossover = ma_data["crossover_detected"]
    ma_crossover_type = ma_data["crossover_type"]
    rsi_value = rsi_data["rsi"]
    rsi_signal = rsi_data["signal"]
    
    # Determine overall signal strength
    signal_strength = 0
    
    # MA contribution
    if "BULLISH" in ma_signal:
        signal_strength += 1
    elif "BEARISH" in ma_signal:
        signal_strength -= 1
        
    # Crossover contribution
    if ma_crossover:
        if "GOLDEN" in ma_crossover_type:
            signal_strength += 2
        elif "DEATH" in ma_crossover_type:
            signal_strength -= 2
            
    # RSI contribution
    if "OVERSOLD" in rsi_signal:
        signal_strength += 1.5
    elif "OVERBOUGHT" in rsi_signal:
        signal_strength -= 1.5
    
    # Determine final recommendation
    if signal_strength >= 2:
        recommendation = "STRONG BUY"
    elif signal_strength > 0:
        recommendation = "BUY"
    elif signal_strength <= -2:
        recommendation = "STRONG SELL"
    elif signal_strength < 0:
        recommendation = "SELL"
    else:
        recommendation = "HOLD"
    
    # Calculate risk level (simple version)
    risk_level = "MEDIUM"
    if abs(signal_strength) > 3:
        risk_level = "LOW"  # Strong signal, lower risk
    elif abs(signal_strength) < 1:
        risk_level = "HIGH"  # Weak signal, higher risk
    
    analysis = f"""# Trading Recommendation for {symbol}

## Summary
Recommendation: {recommendation}
Risk Level: {risk_level}
Signal Strength: {signal_strength:.1f} / 4.5

## Technical Indicators
Moving Averages: {ma_signal}
Recent Crossover: {"Yes - " + ma_crossover_type if ma_crossover else "No"}
RSI ({rsi_data["period"]}): {rsi_value:.2f} - {rsi_signal}

## Reasoning
This recommendation is based on a combination of Moving Average analysis and RSI indicators.
{
    f"The {ma_crossover_type} provides a strong directional signal. " if ma_crossover else ""
}{
    f"The RSI indicates the stock is {rsi_signal.split(' ')[0].lower()}. " if "NEUTRAL" not in rsi_signal else ""
}

## Action Plan
{
    "Consider immediate entry with a stop loss at the recent low. Target the next resistance level." if recommendation == "STRONG BUY" else
    "Look for a good entry point on small dips. Set reasonable stop loss." if recommendation == "BUY" else
    "Consider immediate exit or setting tight stop losses to protect gains." if recommendation == "STRONG SELL" else
    "Start reducing position on strength or set trailing stop losses." if recommendation == "SELL" else
    "Monitor the position but no immediate action needed."
}
"""
    
    return {
        "symbol": symbol,
        "recommendation": recommendation,
        "risk_level": risk_level,
        "signal_strength": signal_strength,
        "ma_signal": ma_signal,
        "rsi_signal": rsi_signal,
        "current_price": ma_data["current_price"],
        "analysis": analysis
    }