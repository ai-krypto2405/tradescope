"""
Binance data fetcher using CCXT
Fetches historical OHLCV data for backtesting
"""
import ccxt
import pandas as pd
from datetime import datetime
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class BinanceDataFetcher:
    """Fetch historical OHLCV data from Binance"""
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """
        Initialize Binance client
        API keys are optional - public endpoints work without authentication
        """
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
            }
        })
    
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        start_date: datetime,
        end_date: datetime,
        limit: int = 1000
    ) -> pd.DataFrame:
        """
        Fetch OHLCV data from Binance
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Candlestick interval (e.g., '1h', '4h', '1d')
            start_date: Start datetime
            end_date: End datetime
            limit: Max candles per request (Binance limit: 1000)
        
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        logger.info(f"Fetching {symbol} {timeframe} data from {start_date} to {end_date}")
        
        # Convert dates to milliseconds timestamp
        since = int(start_date.timestamp() * 1000)
        end_ts = int(end_date.timestamp() * 1000)
        
        all_ohlcv = []
        current_since = since
        
        # Fetch data in chunks (Binance limits to 1000 candles per request)
        while current_since < end_ts:
            try:
                ohlcv = self.exchange.fetch_ohlcv(
                    symbol=symbol,
                    timeframe=timeframe,
                    since=current_since,
                    limit=limit
                )
                
                if not ohlcv:
                    break
                
                all_ohlcv.extend(ohlcv)
                
                # Update since to the last timestamp + 1
                current_since = ohlcv[-1][0] + 1
                
                # Stop if we've reached the end date
                if ohlcv[-1][0] >= end_ts:
                    break
                    
            except Exception as e:
                logger.error(f"Error fetching OHLCV data: {e}")
                raise
        
        # Convert to DataFrame
        df = pd.DataFrame(
            all_ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Filter to exact date range
        df = df[
            (df['timestamp'] >= start_date) &
            (df['timestamp'] <= end_date)
        ]
        
        logger.info(f"Fetched {len(df)} candles")
        return df
    
    def get_available_symbols(self) -> List[str]:
        """Get list of available trading pairs"""
        markets = self.exchange.load_markets()
        return [symbol for symbol in markets.keys() if '/USDT' in symbol]
