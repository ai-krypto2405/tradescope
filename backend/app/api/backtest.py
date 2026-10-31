"""
Backtest API routes
Create, list, and retrieve backtests
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..models.backtest import Backtest, BacktestStatus
from ..schemas.backtest import BacktestCreate, BacktestResponse, BacktestListResponse
from ..utils.auth import get_current_user
from ..tasks.backtest_tasks import run_backtest_task

router = APIRouter(prefix="/api/backtest", tags=["Backtest"])


@router.post("/", response_model=BacktestResponse, status_code=status.HTTP_201_CREATED)
async def create_backtest(
    backtest_data: BacktestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new backtest
    Starts a Celery task to run the backtest asynchronously
    """
    # Create backtest record
    backtest = Backtest(
        user_id=current_user.id,
        name=backtest_data.name,
        symbol=backtest_data.symbol,
        timeframe=backtest_data.timeframe,
        start_date=backtest_data.start_date,
        end_date=backtest_data.end_date,
        strategy_type=backtest_data.strategy_type,
        strategy_params=backtest_data.strategy_params,
        status=BacktestStatus.PENDING
    )
    
    db.add(backtest)
    db.commit()
    db.refresh(backtest)
    
    # Start Celery task
    task = run_backtest_task.delay(backtest.id)
    
    # Update backtest with task ID
    backtest.celery_task_id = task.id
    db.commit()
    
    return BacktestResponse.model_validate(backtest)


@router.get("/", response_model=BacktestListResponse)
async def list_backtests(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all backtests for current user
    Paginated results
    """
    # Get total count
    total = db.query(Backtest).filter(Backtest.user_id == current_user.id).count()
    
    # Get backtests
    backtests = (
        db.query(Backtest)
        .filter(Backtest.user_id == current_user.id)
        .order_by(Backtest.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return BacktestListResponse(
        backtests=[BacktestResponse.model_validate(b) for b in backtests],
        total=total
    )


@router.get("/{backtest_id}", response_model=BacktestResponse)
async def get_backtest(
    backtest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific backtest by ID
    Only returns backtests owned by the current user
    """
    backtest = (
        db.query(Backtest)
        .filter(
            Backtest.id == backtest_id,
            Backtest.user_id == current_user.id
        )
        .first()
    )
    
    if not backtest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backtest not found"
        )
    
    return BacktestResponse.model_validate(backtest)


@router.delete("/{backtest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_backtest(
    backtest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a backtest
    Only allows deletion of backtests owned by the current user
    """
    backtest = (
        db.query(Backtest)
        .filter(
            Backtest.id == backtest_id,
            Backtest.user_id == current_user.id
        )
        .first()
    )
    
    if not backtest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backtest not found"
        )
    
    db.delete(backtest)
    db.commit()
    
    return None
