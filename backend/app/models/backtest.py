"""
Backtest Model
"""
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class BacktestStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Backtest(Base):
    __tablename__ = "backtests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Strategy Config
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)  # e.g., BTC/USDT
    timeframe = Column(String, nullable=False)  # e.g., 1h, 4h, 1d
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Strategy Parameters (stored as JSON)
    strategy_type = Column(String, nullable=False)  # e.g., SMA_CROSSOVER
    strategy_params = Column(JSON, nullable=False)  # e.g., {"fast": 10, "slow": 30}
    
    # Execution
    status = Column(Enum(BacktestStatus), default=BacktestStatus.PENDING)
    celery_task_id = Column(String, nullable=True)
    
    # Results (stored after completion)
    results = Column(JSON, nullable=True)  # Full backtest results
    total_return = Column(Float, nullable=True)
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    win_rate = Column(Float, nullable=True)
    total_trades = Column(Integer, nullable=True)
    
    # Error handling
    error_message = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="backtests")
