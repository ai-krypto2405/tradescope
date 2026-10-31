"""
Stripe integration for payments and subscriptions
"""
import stripe
from typing import Dict, Any, Optional
from ..config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Handle Stripe payments and subscriptions"""
    
    @staticmethod
    def create_checkout_session(
        user_id: int,
        user_email: str,
        price_id: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Create Stripe Checkout session for subscription
        
        Args:
            user_id: User ID to associate with subscription
            user_email: User email
            price_id: Stripe price ID (defaults to config value)
        
        Returns:
            Dict with checkout session URL and session ID
        """
        if not price_id:
            price_id = settings.STRIPE_PRICE_ID
        
        try:
            session = stripe.checkout.Session.create(
                customer_email=user_email,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{settings.FRONTEND_URL}/dashboard?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_URL}/pricing",
                metadata={
                    'user_id': user_id,
                },
                subscription_data={
                    'metadata': {
                        'user_id': user_id,
                    }
                }
            )
            
            logger.info(f"Created checkout session for user {user_id}")
            return {
                "checkout_url": session.url,
                "session_id": session.id
            }
        
        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            raise
    
    @staticmethod
    def create_customer_portal_session(customer_id: str) -> str:
        """
        Create customer portal session for managing subscription
        
        Args:
            customer_id: Stripe customer ID
        
        Returns:
            Portal URL
        """
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=f"{settings.FRONTEND_URL}/dashboard",
            )
            return session.url
        except Exception as e:
            logger.error(f"Error creating portal session: {e}")
            raise
    
    @staticmethod
    def verify_webhook_signature(payload: bytes, signature: str) -> Dict[str, Any]:
        """
        Verify Stripe webhook signature and return event
        
        Args:
            payload: Raw request body
            signature: Stripe signature header
        
        Returns:
            Stripe event object
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            logger.error(f"Invalid payload: {e}")
            raise
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {e}")
            raise
    
    @staticmethod
    def cancel_subscription(subscription_id: str) -> bool:
        """
        Cancel a subscription
        
        Args:
            subscription_id: Stripe subscription ID
        
        Returns:
            True if successful
        """
        try:
            stripe.Subscription.delete(subscription_id)
            logger.info(f"Cancelled subscription {subscription_id}")
            return True
        except Exception as e:
            logger.error(f"Error cancelling subscription: {e}")
            raise
