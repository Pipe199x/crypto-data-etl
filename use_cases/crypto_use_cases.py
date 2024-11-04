from repositories.crypto_repository import CryptoRepository
from datetime import datetime, timedelta
import numpy as np

class GetAllCryptocurrenciesUseCase:
    @staticmethod
    def execute():
        """Fetches all cryptocurrencies."""
        repo = CryptoRepository()
        return repo.get_all_cryptocurrencies()

class GetCryptocurrencyBySymbolUseCase:
    @staticmethod
    def execute(symbol: str):
        """Fetches a cryptocurrency by its symbol."""
        repo = CryptoRepository()
        return repo.get_cryptocurrency_by_symbol(symbol)

class GetHistoricalPricesByCryptoIdUseCase:
    @staticmethod
    def execute(crypto_id: int, start_date: datetime = None, end_date: datetime = None):
        """Fetches historical prices for a given cryptocurrency ID and date range."""
        repo = CryptoRepository()
        return repo.get_historical_prices_by_crypto_id(crypto_id=crypto_id, start_date=start_date, end_date=end_date)

class CalculateCryptoROIUseCase:
    @staticmethod
    def execute(crypto_id: int, start_date: datetime, end_date: datetime):
        """Calculates the ROI for a cryptocurrency between two dates."""
        repo = CryptoRepository()
        initial_price = repo.get_price_on_date(crypto_id, start_date)
        if initial_price is None:
            raise ValueError(f"No price found for the start date: {start_date}")

        final_price = repo.get_price_on_date(crypto_id, end_date)
        if final_price is None:
            raise ValueError(f"No price found for the end date: {end_date}")

        # Calculate the Return on Investment (ROI)
        roi = ((final_price - initial_price) / initial_price) * 100
        return {
            "crypto_id": crypto_id,
            "roi": roi,
            "initial_price": initial_price,
            "final_price": final_price
        }

class GetHighestVolumeCryptoUseCase:
    @staticmethod
    def execute():
        """Fetches the cryptocurrency with the highest volume in the last 24 hours."""
        repo = CryptoRepository()
        return repo.get_highest_volume_crypto()

class CalculateCorrelationUseCase:
    @staticmethod
    def execute(crypto_id_1: int, crypto_id_2: int, days: int = 7):
        """Calculates the correlation between two cryptocurrencies over a specified period."""
        repo = CryptoRepository()

        # Define the date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Fetch historical prices for both cryptocurrencies
        crypto1_prices_data = repo.get_historical_prices_by_crypto_id(crypto_id_1, start_date=start_date, end_date=end_date)
        crypto2_prices_data = repo.get_historical_prices_by_crypto_id(crypto_id_2, start_date=start_date, end_date=end_date)

        if not crypto1_prices_data or not crypto2_prices_data:
            raise ValueError("Insufficient data to calculate correlation")

        # Map dates to prices
        crypto1_prices = {entry.date: entry.close_price for entry in crypto1_prices_data}
        crypto2_prices = {entry.date: entry.close_price for entry in crypto2_prices_data}

        # Find common dates for alignment
        common_dates = set(crypto1_prices.keys()) & set(crypto2_prices.keys())
        if len(common_dates) < 2:
            raise ValueError("Not enough common dates to calculate correlation")

        # Align prices by common dates
        aligned_crypto1_prices = [crypto1_prices[date] for date in sorted(common_dates)]
        aligned_crypto2_prices = [crypto2_prices[date] for date in sorted(common_dates)]

        # Calculate correlation between the two price lists
        correlation = np.corrcoef(aligned_crypto1_prices, aligned_crypto2_prices)[0, 1]
        return {"correlation": correlation, "days": days, "crypto_id_1": crypto_id_1, "crypto_id_2": crypto_id_2}

class CalculateVolatilityUseCase:
    @staticmethod
    def execute():
        """Calculates the volatility of all tracked cryptocurrencies."""
        repo = CryptoRepository()
        all_cryptocurrencies = repo.get_all_cryptocurrencies()

        if not all_cryptocurrencies:
            raise ValueError("No tracked cryptocurrencies found.")

        volatility_results = []
        for crypto in all_cryptocurrencies:
            historical_prices_data = repo.get_historical_prices_by_crypto_id(crypto.id)
            if not historical_prices_data:
                continue

            # Calculate the standard deviation of closing prices as a measure of volatility
            close_prices = [entry.close_price for entry in historical_prices_data]
            if len(close_prices) > 1:
                volatility = np.std(close_prices)
                volatility_results.append({
                    "crypto_id": crypto.id,
                    "coingecko_id": crypto.coingecko_id,
                    "volatility": volatility
                })

        return volatility_results

class CalculateMarketDominanceUseCase:
    @staticmethod
    def execute():
        """Calculates the market dominance for all tracked cryptocurrencies."""
        repo = CryptoRepository()
        all_cryptocurrencies = repo.get_all_cryptocurrencies()

        if not all_cryptocurrencies:
            raise ValueError("No cryptocurrencies found in the database.")

        # Calculate total market cap across all tracked cryptocurrencies
        total_market_cap = sum(crypto.market_cap for crypto in all_cryptocurrencies if crypto.market_cap)

        dominance_results = []
        for crypto in all_cryptocurrencies:
            if crypto.market_cap and total_market_cap > 0:
                # Calculate the market dominance as a percentage of the total market cap
                dominance = (crypto.market_cap / total_market_cap) * 100
                dominance_results.append({
                    "crypto_id": crypto.id,
                    "coingecko_id": crypto.coingecko_id,
                    "dominance": dominance
                })

        return dominance_results

class AnalyzePriceTrendUseCase:
    @staticmethod
    def execute(crypto_id: int, period: int):
        """Analyzes the price trend of a cryptocurrency over a specified period."""
        repo = CryptoRepository()
        historical_prices = repo.get_historical_prices_by_crypto_id(crypto_id)
        if not historical_prices:
            raise ValueError(f"No historical prices found for the cryptocurrency with ID {crypto_id}.")

        # Get the current price
        current_price = historical_prices[-1].close_price
        start_date = datetime.now() - timedelta(days=period)
        price_then = repo.get_price_on_date(crypto_id, start_date)
        
        if price_then is None:
            raise ValueError(f"No price found for {period} days ago.")

        # Determine the trend (upward, downward, or stable)
        trend = "upward" if current_price > price_then else "downward" if current_price < price_then else "stable"
        percentage_change = ((current_price - price_then) / price_then) * 100

        return {
            "crypto_id": crypto_id,
            "current_price": current_price,
            f"price_{period}d_ago": price_then,
            "trend": trend,
            "percentage_change": percentage_change
        }

class ComparePerformanceUseCase:
    @staticmethod
    def execute(crypto_ids: list[int], period: int):
        """Compares the performance of multiple cryptocurrencies over a specified period."""
        repo = CryptoRepository()
        performance = []

        if period < 1:
            raise ValueError("The period must be a positive integer greater than or equal to 1.")

        for crypto_id in crypto_ids:
            historical_prices = repo.get_historical_prices_by_crypto_id(crypto_id)
            if not historical_prices:
                continue

            # Get the current price and price from the specified period ago
            current_price = historical_prices[-1].close_price
            start_date = datetime.now() - timedelta(days=period)
            price_then = repo.get_price_on_date(crypto_id, start_date)
            
            if price_then is None:
                continue

            # Calculate percentage change over the period
            percentage_change = ((current_price - price_then) / price_then) * 100
            performance.append({
                "crypto_id": crypto_id,
                "current_price": current_price,
                f"price_{period}d_ago": price_then,
                "percentage_change": percentage_change
            })

        return performance
