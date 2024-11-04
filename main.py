from fastapi import FastAPI
from config import PORT, HOST
from router.router import router as crypto_router
from etl.coingecko_etl import run_etl
from config import CRYPTOCURRENCIES_TO_FETCH

# Create the FastAPI instance with the title and server configuration
app = FastAPI(title="Cryptocurrency API", host=HOST, port=PORT)

# Include the endpoints from the `crypto_router` in the main application
app.include_router(crypto_router)

# Define a root endpoint (`/`) that returns a welcome message
@app.get("/")
async def root():
    return {"message": "Welcome to the Cryptocurrency Analytics Project! - By Pipe199x"}
