# 🚀 TradeScope Render.com Deployment Guide

## ✅ VORAUSSETZUNGEN
- [x] Code ist fertig
- [x] Git Repository erstellt
- [x] render.yaml konfiguriert
- [ ] GitHub Account
- [ ] Render.com Account

---

## 📝 SCHRITT-FÜR-SCHRITT ANLEITUNG

### Step 1: GitHub Repository erstellen

**Option A: Via GitHub CLI (falls installiert):**
```bash
gh repo create tradescope --public --source=. --remote=origin --push
```

**Option B: Manuell via github.com:**

1. Gehe zu **https://github.com/new**
2. Repository Name: **`tradescope`**
3. Visibility: **Public** (oder Private)
4. **NICHT** "Initialize with README" anklicken
5. Klicke **"Create repository"**

6. Dann im Terminal:
```bash
cd ~/tradescope
git remote add origin https://github.com/DEIN_USERNAME/tradescope.git
git branch -M main
git push -u origin main
```

---

### Step 2: Render.com Account erstellen

1. Gehe zu **https://render.com**
2. Klicke **"Get Started"**
3. **Sign up with GitHub** (empfohlen - einfacher!)
4. Autorisiere Render.com Zugriff auf deine GitHub Repos

---

### Step 3: Backend deployen

1. **Dashboard:** https://dashboard.render.com
2. Klicke **"New +"** → **"Web Service"**
3. **Connect Repository:** Wähle `tradescope`
4. **Settings:**
   - **Name:** `tradescope-backend`
   - **Region:** Frankfurt (EU) oder Oregon (US)
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Starter ($7/month) oder Free (mit Limits)

5. **Environment Variables** (Add):
   ```
   SECRET_KEY = <auto-generate via Render>
   FRONTEND_URL = https://tradescope-frontend.onrender.com
   DEBUG = false
   ```

6. Klicke **"Create Web Service"**
7. ⏳ Warte ~5 Minuten (Build läuft)

---

### Step 4: PostgreSQL Database hinzufügen

1. **Dashboard** → Klicke dein Backend Service
2. **Environment** Tab
3. Scroll runter → **"Add Database"**
4. Wähle **PostgreSQL**
5. **Settings:**
   - **Name:** `tradescope-db`
   - **Plan:** Starter (Free tier verfügbar!)
   - **Region:** Same as backend (Frankfurt)
6. Klicke **"Create Database"**
7. Render fügt automatisch `DATABASE_URL` zu deinen Environment Variables hinzu

---

### Step 5: Frontend deployen (Optional - später)

1. Klicke **"New +"** → **"Static Site"**
2. **Connect Repository:** `tradescope`
3. **Settings:**
   - **Name:** `tradescope-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `.next`
   - **Plan:** Starter ($7/month)

4. **Environment Variables:**
   ```
   NEXT_PUBLIC_API_URL = https://tradescope-backend.onrender.com
   NODE_ENV = production
   ```

5. Klicke **"Create Static Site"**

---

## 🎉 DEPLOYMENT FERTIG!

### Deine URLs:
- **Backend API:** https://tradescope-backend.onrender.com
- **API Docs:** https://tradescope-backend.onrender.com/docs
- **Frontend:** https://tradescope-frontend.onrender.com (wenn deployed)

---

## 📊 KOSTEN-ÜBERSICHT

| Service | Plan | Kosten |
|---------|------|--------|
| Backend (Python) | Starter | $7/Monat |
| Database (PostgreSQL) | Free / Starter | $0 - $7/Monat |
| Frontend (Next.js) | Starter | $7/Monat |
| **TOTAL** | | **$7-21/Monat** |

**Tipp:** Starte nur mit Backend + DB ($7/Monat), Frontend später!

---

## 🔧 NACH DEM DEPLOYMENT

### 1. Teste die API:
```bash
curl https://tradescope-backend.onrender.com/health
# Sollte zurückgeben: {"status":"healthy"}
```

### 2. Öffne API Docs:
```
https://tradescope-backend.onrender.com/docs
```

### 3. Teste Registration:
```bash
curl -X POST https://tradescope-backend.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User"
  }'
```

---

## ⚡ AUTO-DEPLOY AKTIVIEREN

1. **Dashboard** → dein Service → **Settings**
2. **Auto-Deploy:** ON ✅
3. Jetzt deployt jeder `git push` automatisch!

---

## 🐛 TROUBLESHOOTING

### Build schlägt fehl?
- Check **"Logs"** Tab in Render Dashboard
- Meist: fehlende Dependencies in requirements.txt

### Database Connection Error?
- Prüfe `DATABASE_URL` ist gesetzt
- Format: `postgresql://user:pass@host/db`

### Service läuft nicht?
- Check Health Check: `/health` endpoint
- Logs im Dashboard checken

---

## 📞 SUPPORT

- **Render Docs:** https://render.com/docs
- **Render Community:** https://community.render.com
- **Status:** https://status.render.com

---

**Ready to deploy? Start with Step 1!** 🚀
