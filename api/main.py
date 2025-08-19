from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from .db import get_session
from .crud import get_orders_for_date
from .settings import settings

app = FastAPI(title=settings.APP_NAME)

@app.get("/api/status")
async def status():
    return {"ok": True, "app": settings.APP_NAME}

@app.get("/api/order-wins")
async def order_wins(
    date: str = Query(..., description="YYYY-MM-DD (IST date)"),
    exchange: str | None = Query(None, description="Optional: NSE or BSE"),
    session: AsyncSession = Depends(get_session),
):
    try:
        datetime.fromisoformat(date)
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid date; expected YYYY-MM-DD"})
    data = await get_orders_for_date(session, date, exchange)
    return data
