
# Cryptocurrency Analytics API

This project is a FastAPI-based application that provides various endpoints for cryptocurrency analytics, including market dominance, volatility, trend analysis, and performance comparison. The API collects data from the CoinGecko API, stores it in a Supabase database, and exposes endpoints to retrieve and analyze cryptocurrency data.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Schema](#database-schema)
- [Usage](#usage)
  - [Endpoints](#endpoints)
- [ETL Process](#etl-process)
- [Examples](#examples)
- [License](#license)

---

## Features

- Fetches real-time and historical cryptocurrency data from the [CoinGecko API](https://www.coingecko.com/en/api).
- Stores data in Supabase, a scalable backend-as-a-service.
- Provides the following analytical features:
  - Market dominance
  - Volatility
  - Return on Investment (ROI)
  - Trend analysis over a specified period
  - Correlation between cryptocurrencies
  - Performance comparison of multiple cryptocurrencies
  - Fetches the highest volume cryptocurrency in the last 24 hours.

## Requirements

- Python 3.9+
- [Supabase account and project](https://supabase.io/)
- CoinGecko API access

## Installation

Clone the repository:

```bash
git clone https://github.com/Pipe199x/crypto-data-etl
cd crypto-data-etl
```

Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file.

2. Update the `.env` file with your Supabase and CoinGecko API credentials:

   ```
   SUPABASE_API_URL = <your_supabase_url>
   SUPABASE_SERVICE_ROLE_KEY = <your_supabase_service_key>
   COINGECKO_API_KEY = <your_coingecko_api_key>
   COINGECKO_API_URL = https://api.coingecko.com/api/v3
   ```

## Database Schema

The database consists of two main tables:

1. **cryptocurrencies**: Stores the latest data for each tracked cryptocurrency.
   - `id`: Integer (Primary Key)
   - `coingecko_id`: String (Unique identifier for CoinGecko)
   - `symbol`: String (Cryptocurrency symbol)
   - `name`: String (Cryptocurrency name)
   - `current_price`: Float
   - `market_cap`: Float
   - `total_volume`: Float
   - `last_updated`: Timestamp

2. **historical_prices**: Stores historical price data.
   - `id`: UUID (Primary Key)
   - `crypto_id`: Integer (Foreign key to cryptocurrencies table)
   - `coingecko_id`: String
   - `date`: Timestamp (Date of historical price)
   - `close_price`: Float
   - `total_volume`: Float
   - `market_cap`: Float

## Usage

### Starting the API Server

Run the server:

```bash
fastapi dev
```

The API will be available at `http://127.0.0.1:8000`.

### Endpoints

#### General

- **GET /**: Root endpoint to check API status.
- **GET /crypto**: Get all tracked cryptocurrencies.
- **GET /crypto/{symbol}**: Get cryptocurrency by symbol.

#### Analysis

- **GET /crypto/{id}/history**: Fetch historical prices for a cryptocurrency by ID. Accepts optional `start_date` and `end_date` as query parameters.
- **GET /crypto/analysis/roi/{id}**: Calculate ROI for a cryptocurrency over a specific date range.
- **GET /crypto/analysis/volume**: Get the cryptocurrency with the highest volume in the last 24 hours.
- **GET /crypto/analysis/correlation**: Calculate correlation between two cryptocurrencies over a specified period.
- **GET /crypto/analysis/volatility**: Calculate volatility for all tracked cryptocurrencies.
- **GET /crypto/analysis/market-dominance**: Calculate market dominance for each tracked cryptocurrency.
- **GET /crypto/analysis/trend/{id}**: Analyze price trend for a cryptocurrency over a specified period.
- **GET /crypto/analysis/comparison**: Compare performance of multiple cryptocurrencies over a specified period.

### Query Parameters

Some endpoints accept optional query parameters. For example:

- **/crypto/{id}/history**:
  - `start_date`: Start date for the data (format: `YYYY-MM-DD`)
  - `end_date`: End date for the data (format: `YYYY-MM-DD`)

### ETL Process

The ETL (Extract, Transform, Load) process collects data from the CoinGecko API and stores it in Supabase.

- **ETL Configuration**:
  - The ETL process is configured in `run_etl.py` and scheduled to run continuously.
  - Set the cryptocurrencies to fetch in the `.env` file using `CRYPTOCURRENCIES_TO_FETCH`, e.g., `bitcoin, ethereum, usd-coin, solana`.

To run the ETL process once:

```bash
python run_etl.py
```

To run the ETL process continuously:

```bash
python run_etl.py --continuous
```

### Examples

#### Fetch All Cryptocurrencies

```bash
curl http://127.0.0.1:8000/crypto
```

#### Get Cryptocurrency by Symbol

```bash
curl http://127.0.0.1:8000/crypto/btc
```

#### Calculate ROI

```bash
curl "http://127.0.0.1:8000/crypto/analysis/roi/1?start_date=2024-10-01&end_date=2024-11-01"
```

#### Calculate Correlation

```bash
curl "http://127.0.0.1:8000/crypto/analysis/correlation?crypto_id_1=1&crypto_id_2=2&days=7"
```

#### Analyze Price Trend

```bash
curl "http://127.0.0.1:8000/crypto/analysis/trend/1?period=30"
```

#### Compare Performance

```bash
curl "http://127.0.0.1:8000/crypto/analysis/comparison?ids=1&ids=2&period=30"
```

## License

© 2024 Pipe199x. All rights reserved.
