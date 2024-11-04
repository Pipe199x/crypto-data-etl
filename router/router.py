from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from use_cases.crypto_use_cases import (
    GetAllCryptocurrenciesUseCase,
    GetCryptocurrencyBySymbolUseCase,
    GetHistoricalPricesByCryptoIdUseCase,
    CalculateCryptoROIUseCase,
    GetHighestVolumeCryptoUseCase,
    CalculateCorrelationUseCase,
    CalculateVolatilityUseCase,
    CalculateMarketDominanceUseCase,
    AnalyzePriceTrendUseCase,
    ComparePerformanceUseCase,
)

router = APIRouter(prefix="/crypto", tags=["cryptocurrency"])

# Endpoint to get all cryptocurrencies
@router.get("/")
def get_all_cryptocurrencies():
    try:
        return GetAllCryptocurrenciesUseCase.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get a specific cryptocurrency by symbol
@router.get("/{symbol}")
def get_cryptocurrency(symbol: str):
    try:
        crypto = GetCryptocurrencyBySymbolUseCase.execute(symbol)
        if not crypto:
            raise HTTPException(status_code=404, detail="Cryptocurrency not found")
        return crypto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get historical prices by cryptocurrency ID
@router.get("/{id}/history")
def get_historical_prices(
    id: int,
    start_date: datetime = Query(None),
    end_date: datetime = Query(None)
):
    try:
        response = GetHistoricalPricesByCryptoIdUseCase.execute(id, start_date=start_date, end_date=end_date)
        if not response:
            raise HTTPException(status_code=404, detail="No historical prices found for this cryptocurrency")
        return response
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Server error: {str(ex)}")
    
# Example URL: http://127.0.0.1:8000/crypto/1/history?start_date=2024-10-14

# Endpoint to calculate ROI of a cryptocurrency
@router.get("/analysis/roi/{id}")
def calculate_roi(id: int, start_date: str = Query(...), end_date: str = Query(...)):
    try:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        return CalculateCryptoROIUseCase.execute(id, start_date_dt, end_date_dt)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Example URL: http://127.0.0.1:8000/crypto/analysis/roi/1?start_date=2024-10-15&end_date=2024-10-29

# Endpoint to get the cryptocurrency with the highest volume in the last 24 hours
@router.get("/analysis/volume")
def get_highest_volume_crypto():
    try:
        return GetHighestVolumeCryptoUseCase.execute()
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to calculate the correlation between two cryptocurrencies
@router.get("/analysis/correlation")
def calculate_correlation(crypto_id_1: int = Query(...), crypto_id_2: int = Query(...), days: int = Query(7)):
    """
    Calculates the correlation between two specified cryptocurrencies over a given number of days.
    """
    try:
        return CalculateCorrelationUseCase.execute(crypto_id_1, crypto_id_2, days)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Example URL: http://127.0.0.1:8000/crypto/analysis/correlation?crypto_id_1=1&crypto_id_2=2&days=4

# Endpoint to get the volatility of each cryptocurrency
@router.get("/analysis/volatility")
def get_volatility():
    try:
        return CalculateVolatilityUseCase.execute()
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Example URL: http://127.0.0.1:8000/crypto/analysis/volatility

# Endpoint to calculate the market dominance of cryptocurrencies
@router.get("/analysis/market-dominance")
def get_market_dominance():
    try:
        return CalculateMarketDominanceUseCase.execute()
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Example URL: http://127.0.0.1:8000/crypto/analysis/market-dominance

# Endpoint to analyze the price trend of a cryptocurrency
@router.get("/analysis/trend/{id}")
def analyze_price_trend(id: int, period: int = Query(3, gt=0)):
    try:
        return AnalyzePriceTrendUseCase.execute(crypto_id=id, period=period)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Example URL: http://127.0.0.1:8000/crypto/analysis/trend/2

# Endpoint to compare the performance of multiple cryptocurrencies
@router.get("/analysis/comparison")
def compare_performance(ids: list[int] = Query(...), period: int = Query(7, gt=0)):
    try:
        return ComparePerformanceUseCase.execute(crypto_ids=ids, period=period)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example URL: http://127.0.0.1:8000/crypto/analysis/comparison?ids=1&ids=2&period=8
