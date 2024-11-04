import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Supabase and CoinGecko configuration, retrieving keys from environment variables
SUPABASE_URL = os.getenv("SUPABASE_API_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
COINGECKO_API_URL = os.getenv("COINGECKO_API_URL")

# Define the cryptocurrencies to track from the API
CRYPTOCURRENCIES_TO_FETCH = ['bitcoin', 'ethereum', 'usd-coin', 'solana']

# Server configuration
HOST = os.getenv("HOST", "127.0.0.1")  
PORT = int(os.getenv("PORT", 8000)) 
