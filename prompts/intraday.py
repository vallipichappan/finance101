

# # Prompts
# @mcp.prompt()
# def analyze_ticker(symbol: str) -> str:
#     """
#     Analyze a ticker symbol for trading opportunities
#     """
#     return f"""You are a professional stock market analyst. I would like you to analyze the stock {symbol} and provide trading insights.

# Start by examining the current market data and technical indicators. Here are the specific tasks:

# 1. First, check the current market data for {symbol}
# 2. Calculate the moving averages using the calculate_moving_averages tool
# 3. Calculate the RSI using the calculate_rsi tool
# 4. Generate a comprehensive trade recommendation using the trade_recommendation tool
# 5. Based on all this information, provide your professional analysis, highlighting:
#    - The current market position
#    - Key technical indicators and what they suggest
#    - Potential trading opportunities and risks
#    - Your recommended action (buy, sell, or hold) with a brief explanation

# Please organize your response in a clear, structured format suitable for a professional trader."""
 
# @mcp.prompt()
# def compare_tickers(symbols: str) -> str:
#     """
#     Compare multiple ticker symbols for the best trading opportunity
    
#     Args:
#         symbols: Comma-separated list of ticker symbols
#     """
#     symbol_list = [s.strip() for s in symbols.split(",")]
#     symbol_section = "\n".join([f"- {s}" for s in symbol_list])
    
#     return f"""You are a professional stock market analyst. I would like you to compare these stocks and identify the best trading opportunity:

# {symbol_section}

# For each stock in the list, please:

# 1. Check the current market data using the appropriate resource
# 2. Generate a comprehensive trade recommendation using the trade_recommendation tool
# 3. Compare all stocks based on:
#    - Current trend direction and strength
#    - Technical indicator signals
#    - Risk/reward profile
#    - Trading recommendation strength

# After analyzing each stock, rank them from most promising to least promising trading opportunity. Explain your ranking criteria and why you believe the top-ranked stock represents the best current trading opportunity.

# Conclude with a specific recommendation on which stock to trade and what action to take (buy, sell, or hold)."""

# @mcp.prompt()
# def intraday_strategy_builder(symbol: str) -> str:
#     """
#     Build a custom intraday trading strategy for a specific ticker
#     """
#     return f"""You are an expert algorithmic trader specializing in intraday strategies. I want you to develop a custom intraday trading strategy for {symbol}.

# Please follow these steps:

# 1. First, analyze the current market data for {symbol} using the market-data resource
# 2. Calculate relevant technical indicators:
#    - Moving averages (short and long periods)
#    - RSI
# 3. Based on your analysis, design an intraday trading strategy that includes:
#    - Specific entry conditions (technical setups that would trigger a buy/sell)
#    - Exit conditions (both take-profit and stop-loss levels)
#    - Position sizing recommendations
#    - Optimal trading times during the day
#    - Risk management rules

# Make your strategy specific to the current market conditions for {symbol}, not just generic advice. Include exact indicator values and price levels where possible.

# Conclude with a summary of the strategy and how a trader should implement it for today's trading session.""" 
