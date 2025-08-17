from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from typing import Dict

@dataclass
class MarketData:
    symbol: str
    interval: str
    data: pd.DataFrame
    last_updated: datetime

market_data_cache: Dict[str, MarketData] = {}