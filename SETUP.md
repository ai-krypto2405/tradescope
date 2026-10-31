# TradeScope Setup Guide

## 🎯 Complete Setup Instructions

### Step 1: Prerequisites

Install the following:
- **Docker Desktop**: https://www.docker.com/products/docker-desktop
- **Git**: https://git-scm.com/downloads
- **(Optional)** Node.js 20+ & Python 3.11+ for local development

### Step 2: Get Stripe Keys

1. Create a Stripe account: https://dashboard.stripe.com/register
2. Get your **Secret Key**: Dashboard → Developers → API keys
3. Create a **Product** and **Price**: Dashboard → Products → Add Product
   - Name: "TradeScope Premium"
   - Price: $29/month (recurring)
   - Copy the Price ID (starts with `price_`)
4. Set up **Webhook**: Dashboard → Developers → Webhooks
   - Endpoint URL: `http://your-domain.com/api/stripe/webhook`
   - Listen to: `checkout.session.completed`, `customer.subscription.deleted`, `customer.subscription.updated`
   - Copy the Webhook Secret (starts with `whsec_`)

### Step 3: Configure Backend

```bash
cd tradescope/backend
cp .env.example .env
```

Edit `.env`:
```env
STRIPE_SECRET_KEY=sk_test_your_actual_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_actual_secret_here
STRIPE_PRICE_ID=price_your_actual_price_id_here
SECRET_KEY=your-random-secret-key-for-jwt
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Start the Application

#### Option A: Docker Compose (Recommended)

```bash
cd tradescope
./start.sh
```

Or manually:
```bash
docker-compose up --build
```

#### Option B: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Celery (separate terminal):**
```bash
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Step 5: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: PostgreSQL on port 5432
- **Redis**: port 6379

### Step 6: Test the Application

1. **Register**: Create account at http://localhost:3000/register
2. **Create Backtest**:
   - Name: "Test Strategy"
   - Symbol: BTC/USDT
   - Timeframe: 1h
   - Dates: 2024-01-01 to 2024-02-01
   - Strategy: SMA Crossover
   - Fast: 10, Slow: 30
3. **Wait**: Backtest runs in background (check dashboard)
4. **View Results**: Click on completed backtest to see metrics

### Step 7: Subscription Test

1. **Upgrade**: Click "Upgrade to Premium" in dashboard
2. **Stripe Checkout**: Use test card: `4242 4242 4242 4242`
   - Expiry: Any future date
   - CVC: Any 3 digits
3. **Verify**: You should see "Premium" badge in dashboard

## 🔧 Troubleshooting

### Database Connection Error
```bash
docker-compose down -v
docker-compose up --build
```

### Celery Not Running
Check logs:
```bash
docker-compose logs celery-worker
```

### Frontend Can't Connect to Backend
Verify `NEXT_PUBLIC_API_URL` in `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backtest Stuck in "pending"
Restart Celery worker:
```bash
docker-compose restart celery-worker
```

## 📊 Database Access

### Using Docker:
```bash
docker exec -it tradescope-db psql -U tradescope -d tradescope
```

### SQL Commands:
```sql
-- List tables
\dt

-- View users
SELECT * FROM users;

-- View backtests
SELECT id, name, status, total_return FROM backtests;
```

## 🚀 Deployment

### Backend to Railway.app

1. Create Railway account: https://railway.app
2. New Project → Deploy from GitHub
3. Add PostgreSQL addon
4. Set environment variables (from `.env`)
5. Deploy

### Frontend to Vercel

1. Create Vercel account: https://vercel.com
2. Import GitHub repository
3. Framework: Next.js
4. Environment variable: `NEXT_PUBLIC_API_URL` → your Railway backend URL
5. Deploy

### Database Migration

For production, use managed PostgreSQL with TimescaleDB:
- AWS RDS + TimescaleDB extension
- Supabase (PostgreSQL)
- Railway PostgreSQL addon

## 🧪 Testing

### Test Backend API:
```bash
curl http://localhost:8000/health
```

### Test Celery:
```bash
docker-compose logs -f celery-worker
```

### Test Database:
```bash
docker exec tradescope-db pg_isready -U tradescope
```

## 📝 Next Steps

1. **Customize Strategies**: Edit `backend/app/services/backtest_engine.py`
2. **Add More Indicators**: Integrate TA-Lib or pandas-ta
3. **Real-time Data**: Add WebSocket connection to Binance
4. **Advanced Charts**: Use Recharts or TradingView widgets
5. **Alerts**: Email/SMS notifications for completed backtests

## 🤝 Support

- Check `README.md` for API documentation
- Review `docker-compose.yml` for service configuration
- Inspect `.env.example` files for all available settings

## 🎉 You're Ready!

Your TradeScope MVP is now running. Start creating backtests and testing trading strategies!
