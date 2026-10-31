# TradeScope - Trading Backtesting & Strategy Monitor

Professional trading strategy backtesting platform built with FastAPI, Next.js, and TimescaleDB.

## 🚀 Features

- **Historical Data Access**: Fetch OHLCV data from Binance using CCXT
- **Multiple Strategies**: SMA Crossover, RSI, and extensible strategy framework
- **Async Backtesting**: Celery-powered background task processing
- **Detailed Analytics**: Sharpe ratio, max drawdown, win rate, and comprehensive metrics
- **Stripe Integration**: Subscription-based payments
- **Modern UI**: Next.js 15, TypeScript, TailwindCSS, Shadcn/ui

## 🛠️ Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy + PostgreSQL + TimescaleDB
- Celery + Redis
- backtesting.py
- CCXT (Binance API)
- Stripe API

### Frontend
- Next.js 15 (App Router)
- TypeScript
- TailwindCSS
- Shadcn/ui
- Zustand (State Management)
- Axios

## 📦 Quick Start

### Prerequisites
- Docker & Docker Compose
- (Optional) Node.js 20+ and Python 3.11+ for local development

### Run with Docker Compose

1. **Clone and navigate**
   ```bash
   cd tradescope
   ```

2. **Configure environment**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env with your Stripe keys
   
   # Frontend (optional, defaults work)
   # Edit frontend/.env.local if needed
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Services Running

- **PostgreSQL + TimescaleDB**: Port 5432
- **Redis**: Port 6379
- **FastAPI Backend**: Port 8000
- **Celery Worker**: Background tasks
- **Next.js Frontend**: Port 3000

## 🔧 Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if using Alembic)
# alembic upgrade head

# Run FastAPI server
uvicorn app.main:app --reload

# Run Celery worker (separate terminal)
celery -A app.tasks.celery_app worker --loglevel=info
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Backtests
- `POST /api/backtest/` - Create backtest
- `GET /api/backtest/` - List backtests
- `GET /api/backtest/{id}` - Get backtest details
- `DELETE /api/backtest/{id}` - Delete backtest

### Stripe
- `POST /api/stripe/create-checkout-session` - Create checkout
- `POST /api/stripe/customer-portal` - Manage subscription
- `POST /api/stripe/webhook` - Stripe webhooks

## 🎯 Usage Example

### 1. Register & Login
Create an account at http://localhost:3000/register

### 2. Create a Backtest
Fill in the strategy form:
- **Name**: My BTC Strategy
- **Symbol**: BTC/USDT
- **Timeframe**: 1h
- **Date Range**: 2024-01-01 to 2024-03-01
- **Strategy**: SMA Crossover
- **Parameters**: Fast=10, Slow=30

### 3. View Results
The backtest runs asynchronously. Refresh to see:
- Total Return
- Sharpe Ratio
- Max Drawdown
- Win Rate
- Total Trades
- Detailed statistics

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@db:5432/tradescope
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID=price_...
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 Database Schema

### Users
- id, email, username, hashed_password
- is_premium, stripe_customer_id, stripe_subscription_id
- created_at, updated_at

### Backtests
- id, user_id, name, symbol, timeframe
- start_date, end_date, strategy_type, strategy_params
- status, results, metrics
- created_at, completed_at

## 🚢 Deployment

### Backend (Railway.app)
1. Connect GitHub repo
2. Set environment variables
3. Deploy with Dockerfile

### Frontend (Vercel)
1. Import GitHub repo
2. Set `NEXT_PUBLIC_API_URL`
3. Deploy

### Database
- Use Railway PostgreSQL addon
- Or managed PostgreSQL with TimescaleDB

## 🤝 Contributing

This is an MVP. Key improvements:
- [ ] More strategy types
- [ ] Live trading integration
- [ ] Real-time monitoring
- [ ] Advanced charting
- [ ] Portfolio optimization

## 📄 License

MIT

## 🙏 Acknowledgments

- backtesting.py for the backtesting engine
- CCXT for exchange connectivity
- Shadcn/ui for beautiful components
