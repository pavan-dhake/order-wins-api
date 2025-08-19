from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Order
from datetime import date as dt_date

async def get_orders_for_date(session: AsyncSession, date_ymd: str, exchange: str | None = None):
    target = dt_date.fromisoformat(date_ymd)  # '2025-08-19' -> date(2025, 8, 19)

    q = select(Order).where(Order.announcement_date_ist == target)
    if exchange and exchange in ("NSE", "BSE"):
        q = q.where(Order.exchange == exchange)
    q = q.order_by(Order.announcement_time_ist.desc())

    res = await session.execute(q)
    rows = res.scalars().all()
    return [serialize_order(o) for o in rows]

def serialize_order(o: Order) -> dict:
    return {
        "id": str(o.id),
        "company_name": o.company_name,
        "symbol": o.symbol,
        "isin": o.isin,
        "exchange": o.exchange,
        "sector": o.sector,
        "business_unit": o.business_unit,
        "geography": o.geography,
        "order_value_inr": float(o.order_value_inr) if o.order_value_inr is not None else None,
        "currency_original": o.currency_original,
        "original_value": o.original_value_text,
        "value_confidence": o.value_confidence,
        "client_name": o.client_name,
        "order_type": o.order_type,
        "duration": o.duration_text,
        "announcement_time_ist": o.announcement_time_ist.isoformat(),
    }
