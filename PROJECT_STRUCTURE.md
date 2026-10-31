# 📁 TradeScope Project Structure

```
tradescope/
│
├── 📄 README.md                    # Project overview and documentation
├── 📄 SETUP.md                     # Detailed setup instructions
├── 📄 QUICKSTART.md                # 5-minute quick start guide
├── 📄 .gitignore                   # Git ignore rules
├── 📄 docker-compose.yml           # Docker orchestration for all services
├── 🚀 start.sh                     # Quick start script
│
├── 📂 backend/                     # FastAPI Backend
│   ├── 📄 Dockerfile               # Backend Docker image
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 .env.example             # Environment variables template
│   │
│   └── 📂 app/                     # Application code
│       ├── 📄 __init__.py
│       ├── 📄 main.py              # FastAPI app entry point
│       ├── 📄 config.py            # Configuration management
│       ├── 📄 database.py          # Database connection & session
│       │
│       ├── 📂 models/              # SQLAlchemy models
│       │   ├── 📄 __init__.py
│       │   ├── 📄 user.py          # User model (auth, subscription)
│       │   └── 📄 backtest.py      # Backtest model (strategy, results)
│       │
│       ├── 📂 schemas/             # Pydantic schemas (validation)
│       │   ├── 📄 __init__.py
│       │   ├── 📄 user.py          # User request/response schemas
│       │   └── 📄 backtest.py      # Backtest request/response schemas
│       │
│       ├── 📂 api/                 # API routes
│       │   ├── 📄 __init__.py
│       │   ├── 📄 auth.py          # /api/auth/* (register, login, me)
│       │   ├── 📄 backtest.py      # /api/backtest/* (CRUD operations)
│       │   └── 📄 stripe.py        # /api/stripe/* (checkout, webhooks)
│       │
│       ├── 📂 services/            # Business logic
│       │   ├── 📄 __init__.py
│       │   ├── 📄 binance.py       # Binance API client (CCXT)
│       │   ├── 📄 backtest_engine.py  # Backtesting engine (strategies)
│       │   └── 📄 stripe_service.py   # Stripe integration
│       │
│       ├── 📂 tasks/               # Celery background tasks
│       │   ├── 📄 __init__.py
│       │   ├── 📄 celery_app.py    # Celery configuration
│       │   └── 📄 backtest_tasks.py   # Async backtest runner
│       │
│       └── 📂 utils/               # Utilities
│           ├── 📄 __init__.py
│           └── 📄 auth.py          # JWT auth, password hashing
│
├── 📂 frontend/                    # Next.js Frontend
│   ├── 📄 Dockerfile               # Frontend Docker image
│   ├── 📄 package.json             # Node dependencies
│   ├── 📄 tsconfig.json            # TypeScript configuration
│   ├── 📄 tailwind.config.ts       # TailwindCSS configuration
│   ├── 📄 postcss.config.js        # PostCSS configuration
│   ├── 📄 next.config.js           # Next.js configuration
│   ├── 📄 .env.local               # Frontend environment variables
│   ├── 📄 .gitignore               # Frontend-specific ignores
│   ├── 📄 .prettierrc              # Code formatting rules
│   │
│   └── 📂 src/
│       ├── 📂 app/                 # Next.js 15 App Router
│       │   ├── 📄 layout.tsx       # Root layout
│       │   ├── 📄 page.tsx         # Landing page (/)
│       │   ├── 📄 globals.css      # Global styles + Tailwind
│       │   ├── 📂 login/
│       │   │   └── 📄 page.tsx     # Login page (/login)
│       │   ├── 📂 register/
│       │   │   └── 📄 page.tsx     # Register page (/register)
│       │   └── 📂 dashboard/
│       │       └── 📄 page.tsx     # Dashboard (/dashboard)
│       │
│       ├── 📂 components/          # React components
│       │   ├── 📄 StrategyForm.tsx # Backtest creation form
│       │   ├── 📄 ResultsDisplay.tsx  # Backtest results viewer
│       │   └── 📂 ui/              # Shadcn/ui components
│       │       ├── 📄 button.tsx
│       │       ├── 📄 card.tsx
│       │       ├── 📄 input.tsx
│       │       └── 📄 label.tsx
│       │
│       ├── 📂 lib/                 # Utilities & state
│       │   ├── 📄 api.ts           # API client (axios)
│       │   ├── 📄 store.ts         # Zustand state management
│       │   └── 📄 utils.ts         # Helper functions (cn, formatters)
│       │
│       └── 📂 types/               # TypeScript types
│           └── 📄 index.ts         # Shared type definitions
│
└── 🐳 Docker Services (via docker-compose.yml)
    ├── db                          # PostgreSQL + TimescaleDB
    ├── redis                       # Redis (Celery broker)
    ├── backend                     # FastAPI (port 8000)
    ├── celery-worker               # Background task processor
    └── frontend                    # Next.js (port 3000)
```

## 🔑 Key Files Explained

### Backend

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app initialization, CORS, route registration |
| `config.py` | Environment variable management with Pydantic |
| `database.py` | SQLAlchemy engine, session factory, DB initialization |
| `models/*.py` | Database schema (User, Backtest tables) |
| `schemas/*.py` | Request/response validation with Pydantic |
| `api/*.py` | REST API endpoints grouped by feature |
| `services/binance.py` | Fetches OHLCV data from Binance via CCXT |
| `services/backtest_engine.py` | Strategy execution with backtesting.py |
| `services/stripe_service.py` | Stripe checkout, webhooks, subscriptions |
| `tasks/backtest_tasks.py` | Celery task for async backtest execution |
| `utils/auth.py` | JWT token creation, password hashing, auth dependencies |

### Frontend

| File | Purpose |
|------|---------|
| `app/page.tsx` | Landing page with hero, features, pricing |
| `app/login/page.tsx` | User login form |
| `app/register/page.tsx` | User registration form |
| `app/dashboard/page.tsx` | Main app interface (strategy form + backtest list) |
| `components/StrategyForm.tsx` | Form to create new backtest |
| `components/ResultsDisplay.tsx` | Display backtest results & metrics |
| `lib/api.ts` | Axios client with JWT token management |
| `lib/store.ts` | Zustand stores (auth, backtests) |
| `types/index.ts` | TypeScript interfaces for API data |

## 📊 Data Flow

1. **User Registration**:
   - `register/page.tsx` → `api.register()` → `POST /api/auth/register`
   - Backend: `auth.py` → User model → Database
   - Response: JWT token + user data
   - Frontend: Store token in localStorage

2. **Create Backtest**:
   - `StrategyForm.tsx` → `api.createBacktest()` → `POST /api/backtest/`
   - Backend: `backtest.py` → Create DB record → Trigger Celery task
   - Celery: `backtest_tasks.py` → Fetch data → Run strategy → Save results
   - Frontend: Poll for updates or refresh

3. **Stripe Subscription**:
   - Dashboard → `api.createCheckoutSession()` → `POST /api/stripe/create-checkout-session`
   - Backend: `stripe_service.py` → Create Stripe session
   - Redirect user to Stripe Checkout
   - Webhook: Stripe → `POST /api/stripe/webhook` → Update user.is_premium

## 🔌 Service Dependencies

```
Frontend (Next.js)
    ↓ HTTP
Backend (FastAPI)
    ↓
    ├── PostgreSQL (User, Backtest data)
    ├── Redis (Celery message broker)
    └── Celery Worker
            ↓
            ├── Binance API (OHLCV data)
            └── backtesting.py (Strategy execution)
```

## 🚀 Deployment Mapping

| Component | Dev (Docker Compose) | Production |
|-----------|---------------------|------------|
| PostgreSQL | `db` container | Railway PostgreSQL / RDS |
| Redis | `redis` container | Railway Redis / ElastiCache |
| Backend | `backend` container | Railway / Render / Fly.io |
| Celery | `celery-worker` container | Railway / Render Worker |
| Frontend | `frontend` container | Vercel / Netlify |

## 📦 Tech Stack Summary

**Backend**:
- FastAPI (web framework)
- SQLAlchemy (ORM)
- PostgreSQL + TimescaleDB (database)
- Celery + Redis (task queue)
- CCXT (exchange API)
- backtesting.py (strategy engine)
- Stripe API (payments)
- PyJWT (authentication)

**Frontend**:
- Next.js 15 (React framework)
- TypeScript (type safety)
- TailwindCSS (styling)
- Shadcn/ui (components)
- Zustand (state management)
- Axios (HTTP client)

**Infrastructure**:
- Docker Compose (local dev)
- Railway (backend hosting)
- Vercel (frontend hosting)
