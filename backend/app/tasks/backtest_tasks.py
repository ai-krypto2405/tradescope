"""
Celery tasks for backtesting
Runs backtests asynchronously
"""
from datetime import datetime
from sqlalchemy.orm import Session
import logging

from .celery_app import celery_app
from ..database import SessionLocal
from ..models.backtest import Backtest, BacktestStatus
from ..services.binance import BinanceDataFetcher
from ..services.backtest_engine import BacktestingEngine
from ..config import settings

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="tasks.run_backtest")
def run_backtest_task(self, backtest_id: int):
    """
    Celery task to run a backtest
    
    Args:
        backtest_id: ID of the backtest to run
    
    Returns:
        Dict with results or error
    """
    db: Session = SessionLocal()
    
    try:
        # Get backtest from database
        backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
        if not backtest:
            logger.error(f"Backtest {backtest_id} not found")
            return {"error": "Backtest not found"}
        
        # Update status to running
        backtest.status = BacktestStatus.RUNNING
        db.commit()
        
        logger.info(f"Starting backtest {backtest_id}: {backtest.name}")
        
        # Fetch historical data from Binance
        fetcher = BinanceDataFetcher(
            api_key=settings.BINANCE_API_KEY,
            api_secret=settings.BINANCE_API_SECRET
        )
        
        df = fetcher.fetch_ohlcv(
            symbol=backtest.symbol,
            timeframe=backtest.timeframe,
            start_date=backtest.start_date,
            end_date=backtest.end_date
        )
        
        if df.empty:
            raise ValueError("No data fetched from Binance")
        
        logger.info(f"Fetched {len(df)} candles for backtest {backtest_id}")
        
        # Run backtest
        results = BacktestingEngine.run_backtest(
            df=df,
            strategy_type=backtest.strategy_type,
            strategy_params=backtest.strategy_params
        )
        
        # Update backtest with results
        backtest.status = BacktestStatus.COMPLETED
        backtest.results = results
        backtest.total_return = results["total_return"]
        backtest.sharpe_ratio = results["sharpe_ratio"]
        backtest.max_drawdown = results["max_drawdown"]
        backtest.win_rate = results["win_rate"]
        backtest.total_trades = results["total_trades"]
        backtest.completed_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Backtest {backtest_id} completed successfully")
        return results
        
    except Exception as e:
        logger.error(f"Error running backtest {backtest_id}: {e}", exc_info=True)
        
        # Update backtest with error
        if backtest:
            backtest.status = BacktestStatus.FAILED
            backtest.error_message = str(e)
            backtest.completed_at = datetime.utcnow()
            db.commit()
        
        return {"error": str(e)}
        
    finally:
        db.close()
