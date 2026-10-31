"""
Health check endpoint for monitoring
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Simple health check for monitoring services like Render"""
    return {
        "status": "healthy",
        "service": "TradeScope API",
        "version": "1.0.0"
    }
