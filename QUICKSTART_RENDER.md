# 🎯 SCHNELLSTART: GitHub → Render in 5 Minuten

## 1️⃣ GitHub Repository erstellen

**Via Browser:**
1. Gehe zu: https://github.com/new
2. Name: `tradescope`
3. Public
4. Create Repository

**Dann kopiere diese Commands:**

```bash
cd ~/tradescope
git remote add origin https://github.com/DEIN_USERNAME/tradescope.git
git branch -M main
git push -u origin main
```

**❗ WICHTIG:** Ersetze `DEIN_USERNAME` mit deinem GitHub Username!

---

## 2️⃣ Render.com Account

1. **https://render.com** → Get Started
2. **Sign up with GitHub** ✅
3. Autorisiere Render

---

## 3️⃣ Backend deployen

1. **https://dashboard.render.com**
2. **New +** → **Web Service**
3. Connect `tradescope` repo
4. **Einstellungen:**
   ```
   Name: tradescope-backend
   Root Directory: backend
   Runtime: Python 3
   Build: pip install -r requirements.txt
   Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Plan: Starter ($7/month)
   ```
5. **Environment Variables:**
   ```
   SECRET_KEY = [Generate]
   DEBUG = false
   ```
6. **Create Web Service**

---

## 4️⃣ Database hinzufügen

1. Dein Service → **Environment** Tab
2. **Add Database** → PostgreSQL
3. Name: `tradescope-db`
4. Plan: Free
5. Create

✅ `DATABASE_URL` wird automatisch gesetzt!

---

## ✅ FERTIG!

**Deine URL:** https://tradescope-backend.onrender.com

**Teste:**
```bash
curl https://tradescope-backend.onrender.com/health
```

---

## 💰 KOSTEN

**Backend + DB:** $7/Monat (Backend Starter + DB Free)

**Break-Even:** 1 zahlender Kunde ($29/Monat pricing)

---

**Los geht's! Starte mit Schritt 1.** 🚀
