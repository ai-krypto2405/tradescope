# 🚀 TradeScope - Quick Start (5 Minutes)

## 1️⃣ Start Everything

```bash
cd tradescope
./start.sh
```

**OR manually:**
```bash
docker-compose up --build
```

## 2️⃣ Access the App

Open in browser: **http://localhost:3000**

## 3️⃣ Create Account

1. Click "Get Started" or "Sign Up"
2. Fill in: email, username, password
3. Click "Create Account"

## 4️⃣ Run Your First Backtest

Fill in the form:
- **Name**: My First Strategy
- **Symbol**: BTC/USDT
- **Timeframe**: 1h (1 Hour)
- **Start Date**: 2024-01-01
- **End Date**: 2024-02-01
- **Strategy**: SMA Crossover
- **Fast Period**: 10
- **Slow Period**: 30

Click **"Run Backtest"**

## 5️⃣ View Results

- Wait 10-30 seconds for backtest to complete
- Backtest card will show status: COMPLETED
- Click on the backtest to see detailed results:
  - Total Return
  - Sharpe Ratio
  - Max Drawdown
  - Win Rate
  - Total Trades

## 🎉 Done!

You just backtested a trading strategy!

## 📊 What Happens Behind the Scenes?

1. **Frontend** sends backtest request to FastAPI
2. **Backend** creates database record
3. **Celery** picks up the task
4. **Binance API** fetches historical OHLCV data
5. **Backtesting Engine** runs strategy simulation
6. **Results** are saved to database
7. **Dashboard** displays metrics

## 🧪 Test Stripe Subscription

1. Click **"Upgrade to Premium"**
2. Use test card: `4242 4242 4242 4242`
3. Expiry: any future date (e.g., 12/25)
4. CVC: any 3 digits (e.g., 123)
5. Confirm payment
6. See "Premium" badge in dashboard

## 🛑 Stop Everything

```bash
docker-compose down
```

## 📝 Next Steps

- Try different strategies (RSI)
- Adjust parameters
- Test different timeframes
- Explore different symbols (ETH/USDT, etc.)
- Check API docs: http://localhost:8000/docs

## 🔧 Troubleshooting

**Backtest stuck in "pending"?**
```bash
docker-compose restart celery-worker
```

**Can't connect to backend?**
```bash
docker-compose logs backend
```

**Database issues?**
```bash
docker-compose down -v
docker-compose up --build
```

## 🎯 Pro Tips

1. **Shorter date ranges** = faster backtests
2. **1h timeframe** is good for testing
3. **SMA Crossover** is simplest strategy
4. **Fast < Slow** for SMA periods
5. Check **Celery logs** for detailed progress:
   ```bash
   docker-compose logs -f celery-worker
   ```

---

**That's it! Happy backtesting! 📈**
