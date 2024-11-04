from datetime import datetime
from pydantic import BaseModel

# Model for the 'cryptocurrencies' table
class Cryptocurrency(BaseModel):
    id: int | None = None                 # Primary key in the 'cryptocurrencies' table
    coingecko_id: str                     # Unique identifier for CoinGecko
    symbol: str                           # Cryptocurrency symbol, e.g., BTC
    name: str                             # Cryptocurrency name, e.g., Bitcoin
    current_price: float                  # Current price of the cryptocurrency
    market_cap: float                     # Market capitalization
    total_volume: float                   # Total volume of the cryptocurrency
    last_updated: datetime                # Last time the price was updated

# Model for the 'historical_prices' table
class HistoricalPrice(BaseModel):
    id: str                               # UUID in the 'historical_prices' table
    crypto_id: int                        # Reference to 'cryptocurrencies.id'
    coingecko_id: str                     # Unique identifier for CoinGecko
    date: datetime                        # Date of the historical record
    close_price: float                    # Closing price on the specific date
    total_volume: float                   # Total volume on that date
    market_cap: float                     # Market capitalization on that date
