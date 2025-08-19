# Railway Deploy (Order Wins API)

## 1) Create a new service from this repo
- Upload these files to a new GitHub repo (GitHub → New → **Create repository** → **Add file → Upload files** → drag & drop the `order-wins-api.zip` contents).
- In Railway → **New Project** → **Deploy from GitHub Repo** → select your repo.

## 2) Set environment variable
- `DATABASE_URL = postgresql://postgres:[YOUR-PASSWORD]@db.ymuwupomrjllitqmekcs.supabase.co:5432/postgres`

## 3) Set Start Command
- `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

## 4) Deploy and test
- Visit: `https://<your-service>.railway.app/api/status`
- Should return: `{ "ok": true, "app": "order-wins-api" }`

## 5) Optional: Cron for sample ingestion
- In Railway **Schedules/Cron**: run `python -m api.worker.crawler` every 10 minutes.
- Then open: `/api/order-wins?date=2025-08-19` to see the sample row.
