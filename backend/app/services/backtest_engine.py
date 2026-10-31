"""
Backtesting engine - Custom implementation
Implements different trading strategies
"""
import pandas as pd
import numpy as np
import sys
import os

# Import our custom backtesting library
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtesting import Backtest, Strategy
from backtesting_lib import crossover

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class SMAStrategy(Strategy):
    """Simple Moving Average Crossover Strategy"""
    fast_period = 10
    slow_period = 30
    
    def init(self):
        close = self.data['Close']
        self.sma_fast = close.rolling(self.fast_period).mean()
        self.sma_slow = close.rolling(self.slow_period).mean()
    
    def next(self, i):
        if len(self.sma_fast) < 2 or len(self.sma_slow) < 2:
            return
            
        if crossover(self.sma_fast, self.sma_slow):
            self.buy()
        elif crossover(self.sma_slow, self.sma_fast):
            if self.position != 0:
                self.close()


class RSIStrategy(Strategy):
    """RSI Strategy"""
    rsi_period = 14
    rsi_upper = 70
    rsi_lower = 30
    
    def init(self):
        close = self.data['Close']
        self.rsi = self._calculate_rsi(close)
    
    def _calculate_rsi(self, prices):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / (loss + 1e-10)  # Avoid division by zero
        return 100 - (100 / (1 + rs))
    
    def next(self, i):
        if len(self.rsi) < self.rsi_period + 1:
            return
            
        if self.rsi.iloc[-1] < self.rsi_lower:
            self.buy()
        elif self.rsi.iloc[-1] > self.rsi_upper and self.position != 0:
            self.close()


class BacktestingEngine:
    """
    Backtesting engine wrapper
    Executes backtests with different strategies
    """
    
    STRATEGIES = {
        "SMA_CROSSOVER": SMAStrategy,
        "RSI": RSIStrategy,
    }
    
    @staticmethod
    def run_backtest(
        df: pd.DataFrame,
        strategy_type: str,
        strategy_params: Dict[str, Any],
        cash: float = 10000.0,
        commission: float = 0.001  # 0.1% commission
    ) -> Dict[str, Any]:
        """
        Run backtest with given data and strategy
        
        Args:
            df: DataFrame with OHLCV data (columns: timestamp, open, high, low, close, volume)
            strategy_type: Strategy type (SMA_CROSSOVER, RSI, etc.)
            strategy_params: Strategy parameters
            cash: Initial cash
            commission: Trading commission rate
        
        Returns:
            Dictionary with backtest results
        """
        logger.info(f"Running backtest with {strategy_type} strategy")
        
        # Prepare data (requires specific column names with capital letters)
        backtest_df = df.copy()
        backtest_df = backtest_df.rename(columns={
            'timestamp': 'Timestamp',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        })
        
        if 'Timestamp' in backtest_df.columns:
            backtest_df = backtest_df.set_index('Timestamp')
        
        # Get strategy class
        strategy_class = BacktestingEngine.STRATEGIES.get(strategy_type)
        if not strategy_class:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
        
        # Create dynamic strategy class with custom parameters
        class CustomStrategy(strategy_class):
            pass
        
        # Set strategy parameters
        for key, value in strategy_params.items():
            setattr(CustomStrategy, key, value)
        
        # Run backtest
        bt = Backtest(
            backtest_df,
            CustomStrategy,
            cash=cash,
            commission=commission
        )
        
        stats = bt.run()
        
        # Extract key metrics
        results = {
            "total_return": float(stats.get("Return [%]", 0)),
            "sharpe_ratio": float(stats.get("Sharpe Ratio", 0)),
            "max_drawdown": float(stats.get("Max. Drawdown [%]", 0)),
            "win_rate": float(stats.get("Win Rate [%]", 0)),
            "total_trades": int(stats.get("Total Trades", 0)),
            "final_equity": float(stats.get("Equity Final [$]", cash)),
            "initial_equity": float(cash),
            "avg_trade": float(stats.get("Avg. Trade [%]", 0)),
            "detailed_stats": stats
        }
        
        logger.info(f"Backtest completed: {results['total_trades']} trades, {results['total_return']:.2f}% return")
        return results
