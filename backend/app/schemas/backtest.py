"""
Backtest Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List
from ..models.backtest import BacktestStatus


class BacktestCreate(BaseModel):
    """Schema for creating a backtest"""
    name: str = Field(..., min_length=1, max_length=200)
    symbol: str = Field(..., description="Trading pair, e.g., BTC/USDT")
    timeframe: str = Field(..., description="Candlestick timeframe, e.g., 1h, 4h, 1d")
    start_date: datetime
    end_date: datetime
    strategy_type: str = Field(..., description="Strategy type, e.g., SMA_CROSSOVER")
    strategy_params: Dict[str, Any] = Field(..., description="Strategy parameters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "BTC SMA Strategy",
                "symbol": "BTC/USDT",
                "timeframe": "1h",
                "start_date": "2024-01-01T00:00:00",
                "end_date": "2024-03-01T00:00:00",
                "strategy_type": "SMA_CROSSOVER",
                "strategy_params": {
                    "fast_period": 10,
                    "slow_period": 30
                }
            }
        }


class BacktestResponse(BaseModel):
    """Schema for backtest response"""
    id: int
    user_id: int
    name: str
    symbol: str
    timeframe: str
    start_date: datetime
    end_date: datetime
    strategy_type: str
    strategy_params: Dict[str, Any]
    status: BacktestStatus
    celery_task_id: Optional[str]
    
    # Results (available when completed)
    results: Optional[Dict[str, Any]]
    total_return: Optional[float]
    sharpe_ratio: Optional[float]
    max_drawdown: Optional[float]
    win_rate: Optional[float]
    total_trades: Optional[int]
    
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class BacktestListResponse(BaseModel):
    """Schema for list of backtests"""
    backtests: List[BacktestResponse]
    total: int
