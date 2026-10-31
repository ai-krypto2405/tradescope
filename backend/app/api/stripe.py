"""
Stripe API routes
Checkout, webhooks, subscription management
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..utils.auth import get_current_user
from ..services.stripe_service import StripeService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/stripe", tags=["Stripe"])


@router.post("/create-checkout-session")
async def create_checkout_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create Stripe checkout session for subscription
    Returns checkout URL to redirect user
    """
    try:
        result = StripeService.create_checkout_session(
            user_id=current_user.id,
            user_email=current_user.email
        )
        return result
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create checkout session"
        )


@router.post("/customer-portal")
async def create_customer_portal(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create Stripe customer portal session
    Allows user to manage their subscription
    """
    if not current_user.stripe_customer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription found"
        )
    
    try:
        portal_url = StripeService.create_customer_portal_session(
            current_user.stripe_customer_id
        )
        return {"portal_url": portal_url}
    except Exception as e:
        logger.error(f"Error creating portal session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create portal session"
        )


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Stripe webhook events
    Updates user subscription status based on events
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe signature"
        )
    
    try:
        event = StripeService.verify_webhook_signature(payload, sig_header)
    except Exception as e:
        logger.error(f"Webhook signature verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature"
        )
    
    # Handle different event types
    event_type = event["type"]
    data = event["data"]["object"]
    
    logger.info(f"Received Stripe webhook: {event_type}")
    
    if event_type == "checkout.session.completed":
        # Payment successful - activate subscription
        user_id = int(data["metadata"]["user_id"])
        customer_id = data["customer"]
        subscription_id = data.get("subscription")
        
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.stripe_customer_id = customer_id
            user.stripe_subscription_id = subscription_id
            user.is_premium = True
            db.commit()
            logger.info(f"Activated premium for user {user_id}")
    
    elif event_type == "customer.subscription.deleted":
        # Subscription cancelled
        subscription_id = data["id"]
        user = db.query(User).filter(User.stripe_subscription_id == subscription_id).first()
        if user:
            user.is_premium = False
            user.stripe_subscription_id = None
            db.commit()
            logger.info(f"Cancelled premium for user {user.id}")
    
    elif event_type == "customer.subscription.updated":
        # Subscription updated (e.g., payment failed)
        subscription_id = data["id"]
        status_str = data["status"]
        
        user = db.query(User).filter(User.stripe_subscription_id == subscription_id).first()
        if user:
            # Set premium status based on subscription status
            user.is_premium = status_str in ["active", "trialing"]
            db.commit()
            logger.info(f"Updated subscription status for user {user.id}: {status_str}")
    
    return {"status": "success"}
