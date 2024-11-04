from models.cryptocurrency import Cryptocurrency, HistoricalPrice
from database import get_db
from datetime import datetime, timedelta

class CryptoRepository:
    def __init__(self):
        # Initialize the database connection
        self.supabase = get_db()
        print('Database connection established.')

    def get_all_cryptocurrencies(self):
        """Fetches all cryptocurrencies from the database."""
        try:
            # Retrieve all records from the 'cryptocurrencies' table
            response = self.supabase.table('cryptocurrencies').select('*').execute()
            # Return the list of cryptocurrencies as instances of the Cryptocurrency model
            return [Cryptocurrency(**crypto) for crypto in response.data] if response.data else []
        except Exception as e:
            print(f"Error fetching all cryptocurrencies: {e}")
            return []

    def get_cryptocurrency_by_symbol(self, symbol: str):
        """Fetches a specific cryptocurrency by its symbol."""
        try:
            # Query for a cryptocurrency record by symbol
            response = self.supabase.table('cryptocurrencies').select('*').eq('symbol', symbol).execute()
            # Return the cryptocurrency if found, otherwise return None
            return Cryptocurrency(**response.data[0]) if response.data else None
        except Exception as e:
            print(f"Error fetching cryptocurrency by symbol '{symbol}': {e}")
            return None

    def upsert_cryptocurrency(self, crypto: Cryptocurrency):
        """Inserts or updates a cryptocurrency record in the database."""
        # Prepare cryptocurrency data for insertion/updating
        crypto_data = {
            "coingecko_id": crypto.coingecko_id,
            "symbol": crypto.symbol,
            "name": crypto.name,
            "current_price": crypto.current_price,
            "market_cap": crypto.market_cap,
            "total_volume": crypto.total_volume,
            "last_updated": crypto.last_updated.isoformat()
        }
        try:
            # Use upsert to insert or update based on the 'coingecko_id' field
            response = self.supabase.table("cryptocurrencies").upsert(crypto_data, on_conflict=["coingecko_id"]).execute()
            return response
        except Exception as e:
            print(f"Error upserting cryptocurrency '{crypto.symbol}': {e}")
            return None

    def get_historical_prices_by_crypto_id(self, crypto_id: int, start_date=None, end_date=None):
        """
        Fetches historical prices for a given cryptocurrency ID within a specified date range,
        ensuring only unique entries by day.
        """
        # Start with the base query, filtering by 'crypto_id'
        query = (
            self.supabase
            .table("historical_prices")
            .select("*")
            .eq("crypto_id", crypto_id)
        )
        # Add date range filters if provided
        if start_date:
            query = query.gte("date", start_date)
        if end_date:
            query = query.lte("date", end_date)
        
        # Sort results in descending order by date
        query = query.order("date", desc=True)
        response = query.execute()
        
        # Filter to keep only unique entries per day
        unique_data = {}
        for entry in response.data:
            date_key = entry['date'][:10]  # Only use year-month-day for uniqueness
            if date_key not in unique_data:
                unique_data[date_key] = entry

        # Convert each entry to an instance of HistoricalPrice
        return [HistoricalPrice(**data) for data in unique_data.values()]

    def get_price_on_date(self, crypto_id: int, date: datetime):
        """Fetches the closing price of a cryptocurrency on a specific date."""
        # Define the time range for the start and end of the given day
        start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)

        try:
            # Query for the closing price within the specified day range
            query = (
                self.supabase
                .table("historical_prices")
                .select("close_price")
                .eq("crypto_id", crypto_id)
                .gte("date", start_of_day.isoformat())
                .lte("date", end_of_day.isoformat())
                .execute()
            )
            # Return the closing price if data is available, otherwise return None
            return query.data[0]['close_price'] if query.data else None
        except Exception as e:
            print(f"Error fetching price on date '{date}' for crypto ID '{crypto_id}': {e}")
            return None

    def get_highest_volume_crypto(self):
        """Fetches the cryptocurrency with the highest trading volume in the last 24 hours."""
        # Define the cutoff time for the last 24 hours
        last_24_hours = datetime.now() - timedelta(hours=24)

        try:
            # Query for the cryptocurrency with the highest volume within the last 24 hours
            query = (
                self.supabase
                .table("historical_prices")
                .select("crypto_id, coingecko_id, total_volume")
                .gte("date", last_24_hours.isoformat())
                .order("total_volume", desc=True)  # Sort by volume in descending order
                .limit(1)  # Get only the top result
                .execute()
            )
            # Return the highest volume cryptocurrency or None if no data
            return query.data[0] if query.data else None
        except Exception as e:
            print(f"Error fetching highest volume cryptocurrency in the last 24 hours: {e}")
            return None
