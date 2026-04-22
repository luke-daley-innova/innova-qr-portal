# Innova QR Code Portal

A self-service portal for employees to generate QR codes without manual intervention. Connects directly to the Innova QR Code Manager API.

## Deploy to Render (free, recommended)

1. Create a free account at render.com
2. Click **New → Web Service**
3. Connect your GitHub repo (luke-daley-innova/innova-qr-portal)
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Under **Environment Variables**, add:
   - `QR_API_KEY` = `secret:qr.repairsolutions.com:1b1da:ac68125cf702df4afbb860031be954b5`
6. Click **Deploy** — Render gives you a public URL to share with employees.

## Run locally (for testing)

```bash
pip install -r requirements.txt
export QR_API_KEY="secret:qr.repairsolutions.com:1b1da:ac68125cf702df4afbb860031be954b5"
python app.py
```

Then open http://localhost:5000 in your browser.

## Files

| File | Purpose |
|------|---------|
| `app.py` | Flask backend — proxies requests to the QR API |
| `templates/index.html` | Employee-facing portal UI |
| `requirements.txt` | Python dependencies |
| `Procfile` | Tells Render/Heroku how to start the app |
