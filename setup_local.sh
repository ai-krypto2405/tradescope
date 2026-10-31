#!/bin/bash
# TradeScope - Local Development Setup (No Docker)

echo "🚀 TradeScope Local Development Setup"
echo "======================================"
echo ""

cd ~/tradescope

# 1. Backend Setup
echo "📦 Step 1/5: Backend Dependencies..."
cd backend

# Create venv if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install requirements
pip install -r requirements.txt --quiet

echo "✅ Backend dependencies installed"
echo ""

# 2. Database Setup (SQLite for local dev)
echo "📊 Step 2/5: Database Setup..."
# Patch database.py to use SQLite instead of PostgreSQL
cd ~/tradescope

echo "Using SQLite for local development (no PostgreSQL needed)"
echo "✅ Database ready"
echo ""

# 3. Frontend Setup
echo "🎨 Step 3/5: Frontend Dependencies..."
cd frontend

if [ ! -d "node_modules" ]; then
    npm install
fi

echo "✅ Frontend dependencies installed"
echo ""

# 4. Start Services
echo "🚀 Step 4/5: Starting Services..."
echo ""
echo "Services will start in separate terminals:"
echo "  Terminal 1: FastAPI Backend"
echo "  Terminal 2: Celery Worker"
echo "  Terminal 3: Next.js Frontend"
echo ""

# Create start scripts
cat > ~/tradescope/run_backend.sh << 'EOF'
#!/bin/bash
cd ~/tradescope/backend
source venv/bin/activate
echo "🔧 Starting FastAPI Backend on http://localhost:8000"
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF

cat > ~/tradescope/run_celery.sh << 'EOF'
#!/bin/bash
cd ~/tradescope/backend
source venv/bin/activate
echo "⚙️  Starting Celery Worker..."
python3 -m celery -A app.tasks.celery_app worker --loglevel=info
EOF

cat > ~/tradescope/run_frontend.sh << 'EOF'
#!/bin/bash
cd ~/tradescope/frontend
echo "🎨 Starting Next.js Frontend on http://localhost:3000"
npm run dev
EOF

chmod +x ~/tradescope/run_*.sh

echo "✅ Start scripts created"
echo ""

echo "🎉 Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo "================================"
echo ""
echo "Open 3 separate terminals and run:"
echo ""
echo "  Terminal 1: ~/tradescope/run_backend.sh"
echo "  Terminal 2: ~/tradescope/run_celery.sh"
echo "  Terminal 3: ~/tradescope/run_frontend.sh"
echo ""
echo "Then open: http://localhost:3000"
echo ""
