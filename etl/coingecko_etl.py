import requests
import time
from datetime import datetime, timedelta
from database import get_db
from config import COINGECKO_API_URL
from repositories.crypto_repository import CryptoRepository
from models.cryptocurrency import Cryptocurrency

# Fetch current cryptocurrency data from the CoinGecko API
def fetch_crypto_data(crypto_id):
    try:
        response = requests.get(f"{COINGECKO_API_URL}/coins/{crypto_id}")
        response.raise_for_status()  # Raises an exception for HTTP error codes (4XX/5XX)
        data = response.json()
        
        # Check that the response contains the 'id' key
        if 'id' not in data:
            raise KeyError(f"'id' key not found in response for {crypto_id}. Full response: {data}")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Network error when fetching data for {crypto_id}: {str(e)}")
        time.sleep(5)  # Wait 5 seconds before retrying
        return fetch_crypto_data(crypto_id)  # Retry the request

# Fetch historical price data from the CoinGecko API
def fetch_historical_data(crypto_id, days=5):
    try:
        response = requests.get(
            f"{COINGECKO_API_URL}/coins/{crypto_id}/market_chart",
            params={
                "vs_currency": "usd",  # Reference currency
                "days": days,          # Time period in days
                "interval": "daily"    # Daily data
            }
        )
        response.raise_for_status()
        data = response.json()

        # Verify that the data includes the 'prices' key
        if "prices" not in data:
            raise KeyError(f"'prices' key not found in historical data for {crypto_id}. Full response: {data}")

        return data
    except requests.exceptions.RequestException as e:
        print(f"Network error when fetching historical data for {crypto_id}: {str(e)}")
        time.sleep(5)  # Wait 5 seconds before retrying
        return fetch_historical_data(crypto_id, days)

# Transform the current cryptocurrency data into a database model
def transform_crypto_data(raw_data):
    # Validate the data structure
    if 'market_data' not in raw_data or 'current_price' not in raw_data['market_data']:
        raise KeyError(f"Missing 'market_data' or 'current_price' in response. Full response: {raw_data}")
    
    return Cryptocurrency(
        coingecko_id=raw_data["id"],
        symbol=raw_data["symbol"].upper(),
        name=raw_data["name"],
        current_price=raw_data["market_data"]["current_price"]["usd"],
        market_cap=raw_data["market_data"]["market_cap"]["usd"],
        total_volume=raw_data["market_data"]["total_volume"]["usd"],
        last_updated=datetime.now()
    )

# Transform the historical data into a format suitable for the 'historical_prices' table
def transform_historical_data(raw_data, crypto_id, coingecko_id):
    # Validate the presence of the 'prices' key in the data
    if "prices" not in raw_data or not raw_data["prices"]:
        raise KeyError(f"Data from API is missing 'prices'. Raw data: {raw_data}")
    
    return [
        {
            "crypto_id": crypto_id,
            "coingecko_id": coingecko_id,
            "date": datetime.fromtimestamp(price[0] / 1000).isoformat(),  # Convert date to ISO format
            "close_price": price[1],
            "total_volume": volume[1],
            "market_cap": market_cap[1]
        }
        for price, market_cap, volume in zip(
            raw_data["prices"],
            raw_data["market_caps"],
            raw_data["total_volumes"]
        )
    ]

# Load the transformed cryptocurrency data into the database
def load_crypto_data(data):
    repo = CryptoRepository()
    result = repo.upsert_cryptocurrency(data)
    
    # Access the first element in result.data
    return result.data[0]['id']

# Insert the transformed historical data into the 'historical_prices' table
def load_historical_data(data):
    db = get_db()
    print("Data to be inserted:", data)
    db.table("historical_prices").insert(data).execute()

# Main ETL function that coordinates the process for each cryptocurrency in the list
def run_etl(crypto_ids):
    for crypto_id in crypto_ids:
        try:
            # Step 1: Extract data from the API
            crypto_data = fetch_crypto_data(crypto_id)
            historical_data = fetch_historical_data(crypto_id)

            # Step 2: Transform the extracted data
            transformed_crypto = transform_crypto_data(crypto_data)

            # Step 3: Load cryptocurrency data and get its ID in the database
            db_crypto_id = load_crypto_data(transformed_crypto)

            # Get coingecko_id for historical data
            coingecko_id = transformed_crypto.coingecko_id

            # Transform and load historical data
            transformed_history = transform_historical_data(historical_data, db_crypto_id, coingecko_id)
            load_historical_data(transformed_history)

            print(f"ETL process for {crypto_id} completed successfully.")

        except Exception as e:
            print(f"Error during ETL process for {crypto_id}: {str(e)}")

    print("ETL process completed for all cryptocurrencies.")
