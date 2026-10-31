"""
Simple Backtest Engine (Custom Implementation)
Replaces the external 'backtesting' library
"""
from typing import Callable, Dict, List, Optional
from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class Trade:
    entry_time: pd.Timestamp
    entry_price: float
    exit_time: Optional[pd.Timestamp] = None
    exit_price: Optional[float] = None
    size: float = 1.0
    is_long: bool = True
    
    @property
    def pnl(self) -> float:
        if self.exit_price is None:
            return 0.0
        if self.is_long:
            return (self.exit_price - self.entry_price) * self.size
        else:
            return (self.entry_price - self.exit_price) * self.size
    
    @property
    def pnl_pct(self) -> float:
        if self.exit_price is None:
            return 0.0
        if self.is_long:
            return ((self.exit_price - self.entry_price) / self.entry_price) * 100
        else:
            return ((self.entry_price - self.exit_price) / self.entry_price) * 100


class Strategy:
    """
    Base Strategy class
    Subclass this and implement init() and next() methods
    """
    def __init__(self, broker, data):
        self.broker = broker
        self.data = data
        
    def init(self):
        """Initialize indicators - override this"""
        pass
    
    def next(self, i):
        """Called for each bar - override this"""
        pass
    
    def buy(self, size=1.0):
        """Open a long position"""
        return self.broker.buy(size)
    
    def sell(self, size=1.0):
        """Open a short position"""
        return self.broker.sell(size)
    
    def close(self):
        """Close current position"""
        return self.broker.close()
    
    @property
    def position(self):
        """Current position"""
        return self.broker.position


class SimpleBroker:
    """Simulated broker for backtesting"""
    def __init__(self, data: pd.DataFrame, cash: float = 10000, commission: float = 0.001):
        self.data = data
        self.initial_cash = cash
        self.cash = cash
        self.commission = commission
        self.current_position = None
        self.trades: List[Trade] = []
        
    def buy(self, size=1.0):
        """Open long position"""
        if self.current_position is not None:
            return  # Already in position
        
        price = self.data['Close'].iloc[-1]
        cost = price * size * (1 + self.commission)
        
        if cost > self.cash:
            return  # Insufficient funds
        
        self.cash -= cost
        self.current_position = Trade(
            entry_time=self.data.index[-1],
            entry_price=price,
            size=size,
            is_long=True
        )
        
    def sell(self, size=1.0):
        """Open short position"""
        if self.current_position is not None:
            return  # Already in position
            
        price = self.data['Close'].iloc[-1]
        self.current_position = Trade(
            entry_time=self.data.index[-1],
            entry_price=price,
            size=size,
            is_long=False
        )
        
    def close(self):
        """Close current position"""
        if self.current_position is None:
            return
            
        price = self.data['Close'].iloc[-1]
        self.current_position.exit_time = self.data.index[-1]
        self.current_position.exit_price = price
        
        # Calculate PnL
        pnl = self.current_position.pnl
        cost = price * self.current_position.size * self.commission
        
        if self.current_position.is_long:
            self.cash += (price * self.current_position.size) - cost
        else:
            self.cash += (self.current_position.entry_price * 2 * self.current_position.size) - (price * self.current_position.size) - cost
        
        self.trades.append(self.current_position)
        self.current_position = None
        
    @property
    def position(self):
        """Current position (1 for long, -1 for short, 0 for none)"""
        if self.current_position is None:
            return 0
        return 1 if self.current_position.is_long else -1
    
    @property
    def equity(self) -> float:
        """Current account equity"""
        equity = self.cash
        if self.current_position is not None:
            current_price = self.data['Close'].iloc[-1]
            if self.current_position.is_long:
                equity += current_price * self.current_position.size
            else:
                equity += (self.current_position.entry_price - current_price) * self.current_position.size
        return equity


class Backtest:
    """
    Backtesting engine
    Compatible interface with the 'backtesting' library
    """
    def __init__(self, data: pd.DataFrame, strategy: type, cash: float = 10000, commission: float = 0.001):
        self.data = data
        self.strategy_class = strategy
        self.cash = cash
        self.commission = commission
        self.results = None
        
    def run(self, **kwargs) -> Dict:
        """Run the backtest"""
        # Create broker
        broker = SimpleBroker(self.data, cash=self.cash, commission=self.commission)
        
        # Create strategy instance
        strategy = self.strategy_class(broker, self.data)
        strategy.init()
        
        # Run through all bars
        equity_curve = []
        for i in range(len(self.data)):
            # Update broker's view of data (sliding window)
            broker.data = self.data.iloc[:i+1]
            
            # Call strategy
            strategy.next(i)
            
            # Record equity
            equity_curve.append(broker.equity)
        
        # Close any open position at the end
        if broker.current_position is not None:
            broker.close()
        
        # Calculate statistics
        equity_curve = pd.Series(equity_curve, index=self.data.index)
        returns = equity_curve.pct_change().dropna()
        
        winning_trades = [t for t in broker.trades if t.pnl > 0]
        losing_trades = [t for t in broker.trades if t.pnl <= 0]
        
        total_pnl = sum(t.pnl for t in broker.trades)
        total_return_pct = ((broker.equity - self.cash) / self.cash) * 100
        
        max_drawdown = 0
        peak = equity_curve[0]
        for value in equity_curve:
            if value > peak:
                peak = value
            drawdown = ((peak - value) / peak) * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        self.results = {
            'Start': self.data.index[0],
            'End': self.data.index[-1],
            'Duration': self.data.index[-1] - self.data.index[0],
            'Equity Final [$]': broker.equity,
            'Equity Peak [$]': equity_curve.max(),
            'Return [%]': total_return_pct,
            'Total Trades': len(broker.trades),
            'Win Rate [%]': (len(winning_trades) / len(broker.trades) * 100) if broker.trades else 0,
            'Max. Drawdown [%]': max_drawdown,
            'Avg. Trade [%]': np.mean([t.pnl_pct for t in broker.trades]) if broker.trades else 0,
            'Sharpe Ratio': (returns.mean() / returns.std() * np.sqrt(252)) if len(returns) > 0 and returns.std() > 0 else 0,
            'Sortino Ratio': (returns.mean() / returns[returns < 0].std() * np.sqrt(252)) if len(returns[returns < 0]) > 0 else 0,
            '_trades': broker.trades,
            '_equity_curve': equity_curve,
        }
        
        return self.results
    
    def plot(self):
        """Plot results (placeholder - would need matplotlib)"""
        print("📊 Plotting not implemented in custom engine")
        if self.results:
            print(f"Equity curve available with {len(self.results['_equity_curve'])} data points")
